# Fix: message being sent leaks into another chat's compose/draft, and erases what is typed there

Branch: `nd/fix-inflight-send-writes-other-chat-compose` (off `origin/master`)
Date: 2026-07-25

Line references are against `origin/master` at `c7e83d88a`, with this fix
applied. Android and desktop (`commonMain`); iOS not addressed.

## Problem

Two reported symptoms, one cause. Both need a send that is still in
flight when the chat is switched (slow network, large file, or the send
just hanging with the progress circle showing):

1. **The message ends up in another chat's draft.** Reply to a message
   (or just type), press send, switch to another chat while it is
   sending: the text *and the reply context* appear in that chat's input,
   and leaving it saves them as that chat's draft. No forwarding
   involved.
2. **A late send erases what you typed.** Press send, the progress circle
   keeps spinning, switch to another chat and back, type a new message —
   when the original send finally succeeds, the newly typed message is
   erased.

## Cause

The compose state is shared, and the send outlives the chat:

- `ChatView.kt:134` — one `MutableState<ComposeState>` per `ChatView`
  instance, `rememberSaveable` with no keys, reused for every chat that
  the view displays.
- `Utils.kt:43-46` — `withLongRunningApi` launches on
  `CoroutineScope(Dispatchers.Default)`, a standalone scope with no tie
  to the composition or to the chat, and `sendMessage`
  (`ComposeView.kt:958-962`) uses it. Leaving the chat never cancels an
  in-flight send.

Two writes then act on the wrong chat:

- **On the chat switch** — `ComposeView.kt:1329-1333`: the `cs.inProgress`
  branch used to keep the message in the shared compose state
  (`composeState.value = cs.copy(inProgress = false, progressByTimeout = false)`)
  and only cleared the *previous* chat's saved draft. The text and the
  quote were therefore sitting in the input of the chat opened next, and
  `ComposeView.kt:1334-1344` (`!cs.empty`) then saved them as *that*
  chat's draft on the next switch. Symptom 1.
- **When the send completes** — `ComposeView.kt:937-943`, running in the
  detached coroutine after the switch: `clearState(live)` on success, or
  `composeState.value = lastFailed` on failure, where `lastFailed =
  cs.copy(inProgress = false, preview = preview)`
  (`ComposeView.kt:723`) **keeps `contextItem`, i.e. the reply**. On
  success this wipes whatever is in the input now — including a message
  typed after coming back (symptom 2); on failure it dumps the old
  message into whichever chat is open (symptom 1 again).

The same function was already inconsistent about which chat it acts on:
its draft bookkeeping (`clearCurrentDraft()`, and the forwarding
condition) uses the **captured** `chat` — the chat the message was
composed in — while its `composeState` writes hit whatever chat is
displayed at that moment.

## Fix

Two changes, both in `ComposeView.kt`.

**1. Do not keep the message being sent in the shared compose state**
(`ComposeView.kt:1329-1333`). On switching away with a send in flight the
compose state is cleared, so nothing leaks into the chat opened next:

```kotlin
} else if (cs.inProgress) {
  clearPrevDraft(prevChatId)
  // the message being sent must not be kept in the compose state, it is shared with the chat opened next;
  // if it fails to send it is saved as the draft of the chat it was composed in
  composeState.value = ComposeState(useLinkPreviews = useLinkPreviews)
}
```

In-flight content is deliberately **not** saved as a draft here: the
message has been submitted and will most likely be sent, and a draft is
for messages that are not sent yet.

**2. Only touch the compose state if it still holds the message that was
sent** (`ComposeView.kt:932-954`):

```kotlin
val stillComposingSentMessage = composeState.value.inProgress && (chatModel.chatId.value == chat.id || cs.liveMessage != null)
if (stillComposingSentMessage) {
  if (lastFailed == null) clearState(live) else composeState.value = lastFailed
}
val draft = chatModel.draft.value
if (stillComposingSentMessage && wasForwarding && ...) {
  composeState.value = draft
} else {
  clearCurrentDraft()
  // the message was not sent, so it is kept as the draft of the chat it was composed in instead of being restored into another chat
  if (!stillComposingSentMessage && lastFailed != null && saveLastDraft) {
    chatModel.draft.value = lastFailed
    chatModel.draftChatId.value = chat.id
  }
}
```

`inProgress` is the marker that the compose state is still the submitted
message: it is set by `sending()` (`ComposeView.kt:594-596`), preserved by
`copy` while sending (the only other write during a send is
`progressByTimeout` at `ComposeView.kt:1582-1589`), reset when switching
away (change 1), and never set by typing a new message. So a chat switch
*or* newly typed text both make the guard false.

A **failed** send is different from an in-flight one — the message was
not sent, so it is an unsent message and belongs in the draft of the chat
it was composed in, which is where the user can find and resend it. This
also keeps the "preserving long message when failed to send" behaviour
(`e61babdc8`) working when the user stays in the chat: the guard is true
there and the failed message is restored into the input as before.

`cs.liveMessage != null` is part of the guard because a live message is
sent *because* the chat is being left (`ComposeView.kt:1324-1328`), and
that branch deliberately leaves the compose state for the send to clear.
`sendMessageAsync` reads `composeState` inside the coroutine
(`ComposeView.kt:678`), so that branch cannot clear the state itself
without racing the send — the guard keeps today's behaviour for it
instead of changing it.

Blast radius: no new state, no new lifecycle. The clear/restore that
already ran now runs only when the compose state still belongs to the
sent message; the only added write is the failed-message draft, gated on
`saveLastDraft`.

## Behaviour after the fix

| situation | before | after |
| --- | --- | --- |
| send, stay in chat, succeeds | input cleared | input cleared (unchanged) |
| send, stay in chat, fails | message restored in input | message restored in input (unchanged) |
| send, switch chats, succeeds | message left in the other chat's input, saved as its draft | other chat untouched |
| send, switch chats, fails | message dumped into the other chat's input | message saved as the draft of the chat it was composed in |
| send hangs, switch away and back, type, then it succeeds | typed message erased | typed message kept |
| forward send, still in destination chat | destination chat's draft restored | unchanged |
| live message sent on leaving the chat | compose state cleared by the send | unchanged |

## Verification

- `./gradlew :common:compileKotlinDesktop` — passes.
- Manual (needs a slow or failing send — e.g. airplane mode, or a large
  file):
  1. Reply + type in A, send, switch to B while sending. B's input must
     stay empty; leaving B must not create a draft in B. If the send
     failed, A must hold the message (with the reply) as its draft.
  2. Send in A with the network off so the circle keeps spinning, switch
     to B and back to A, type a new message, restore the network. The
     typed message must survive the old send completing.
  3. Regression: ordinary send in A (input clears), failed send while
     staying in A (message comes back in the input), forward into a chat
     that has a draft (draft restored after sending).

Related: `plans/2026-07-25-fix-forward-moves-draft-to-target-chat.md`
(PR #7307) — different cause (stale `chat` captured by the desktop
`onDispose`), same shared-compose-state design.
