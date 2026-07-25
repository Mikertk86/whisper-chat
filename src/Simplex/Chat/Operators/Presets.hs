{-# LANGUAGE DataKinds #-}
{-# LANGUAGE DuplicateRecordFields #-}
{-# LANGUAGE OverloadedLists #-}
{-# LANGUAGE OverloadedStrings #-}

module Simplex.Chat.Operators.Presets where

import Data.List.NonEmpty (NonEmpty)
import qualified Data.List.NonEmpty as L
import Simplex.Chat.Operators
import Simplex.Messaging.Agent.Env.SQLite (ServerRoles (..), allRoles)
import Simplex.Messaging.Agent.Store.Entity
import Simplex.Messaging.Protocol (ProtocolType (..), SMPServer)

whisperSMPServer :: SMPServer
whisperSMPServer = "smp://0zCvaMgX0nL95J68oW7dyWrIVpMGyhbqyqbC2ekemHA=@100.84.65.50:5223"

operatorSimpleXChat :: NewServerOperator
operatorSimpleXChat =
  ServerOperator
    { operatorId = DBNewEntity,
      operatorTag = Just OTSimplex,
      tradeName = "Whisper",
      legalName = Just "Whisper private relay",
      serverDomains = ["100.84.65.50", "tailb34dd3.ts.net"],
      conditionsAcceptance = CAAccepted Nothing True,
      enabled = True,
      smpRoles = allRoles,
      xftpRoles = allRoles
    }

operatorFlux :: NewServerOperator
operatorFlux =
  ServerOperator
    { operatorId = DBNewEntity,
      operatorTag = Just OTFlux,
      tradeName = "Whisper Legacy Disabled",
      legalName = Just "Whisper",
      serverDomains = [],
      conditionsAcceptance = CAAccepted Nothing True,
      enabled = False,
      smpRoles = ServerRoles {storage = False, proxy = False},
      xftpRoles = ServerRoles {storage = False, proxy = False}
    }

allPresetServers :: NonEmpty SMPServer
allPresetServers = enabledSimplexChatSMPServers

simplexChatSMPServers :: [NewUserServer 'PSMP]
simplexChatSMPServers = map (presetServer' True) (L.toList enabledSimplexChatSMPServers)

enabledSimplexChatSMPServers :: NonEmpty SMPServer
enabledSimplexChatSMPServers = [whisperSMPServer]

disabledSimplexChatSMPServers :: NonEmpty SMPServer
disabledSimplexChatSMPServers = [whisperSMPServer]

simplexChatRelays :: [NewUserChatRelay]
simplexChatRelays = []

fluxSMPServers :: [NewUserServer 'PSMP]
fluxSMPServers = []

fluxSMPServers_ :: NonEmpty SMPServer
fluxSMPServers_ = [whisperSMPServer]

whisperXFTPServers :: [NewUserServer 'PXFTP]
whisperXFTPServers = map (presetServer True) ["xftp://O5SdqMMNz6c5ceFrpY5mh4kyYYuD9vUze3-uMeJ9c6o=@100.84.65.50:5443"]

fluxXFTPServers :: [NewUserServer 'PXFTP]
fluxXFTPServers = []
