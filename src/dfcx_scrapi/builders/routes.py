"""A set of builder methods to create CX proto resource objects"""

# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import List, Dict, Union, Any

from google.cloud.dialogflowcx_v3beta1 import types
from google.protobuf import struct_pb2


class FulfillmentBuilder:
    """Base Class for CX Fulfillment builder."""


    def __init__(self, obj: types.Fulfillment = None):
        self.proto_obj = None
        if obj:
            self.load_fulfillment(obj)


    def _check_fulfillment_exist(self):
        """Check if the proto_obj exists otherwise raise an error."""

        if not self.proto_obj:
            raise ValueError(
                "There is no proto_obj!"
                "\nUse create_empty_fulfillment or load_fulfillment to continue."
            )
        elif not isinstance(self.proto_obj, types.Fulfillment):
            raise ValueError(
                "proto_obj is not a Fulfillment type."
                "\nPlease create or load the correct type to continue."
            )


    def load_fulfillment(
        self, obj: types.Fulfillment, overwrite: bool = False
    ) -> types.Fulfillment:
        """Load an existing Fulfillment to proto_obj for further uses.

        Args:
          obj (Fulfillment):
            An existing Fulfillment obj.
          overwrite (bool)
            Overwrite the new proto_obj if proto_obj already
            contains a Fulfillment.

        Returns:
          A Fulfillment object stored in proto_obj
        """
        if not isinstance(obj, types.Fulfillment):
            raise ValueError(
                "The object you're trying to load is not a Fulfillment!"
            )

        if self.proto_obj and not overwrite:
            raise Exception(
                "proto_obj already contains a Fulfillment."
                " If you wish to overwrite it, pass overwrite as True."
            )

        if overwrite or not self.proto_obj:
            self.proto_obj = obj

        return self.proto_obj


    def _response_message_creator(
        response_type: str,
        message: Union[str, List[str], Dict[str, Any]],
        mode: str = None
    ) -> types.ResponseMessage:
        """Represents a response message that can be returned by a
        conversational agent.
        Response messages are also used for output audio synthesis.

        Args:
            response_type (str):
                Type of the response message. It should be one of the following:
                'text', 'live_agent_handoff', 'conversation_success',
                'output_audio_text', 'play_audio', 'telephony_transfer_call'
            message (str | List[str] | Dict[str, str]):
                The output message. For each response_type
                it should be formatted like the following:
                    text --> str | List[str]
                    live_agent_handoff --> Dict[str, Any]
                    conversation_success --> Dict[str, Any]
                    output_audio_text --> str
                    play_audio --> str
                    telephony_transfer_call --> str
            mode (str):
                This argument is only applicable for 'output_audio_text'.
                It should be one of the following: 'text', 'ssml'

        Returns:
            A ResponseMessage object
        """
        if response_type == "text":
            if isinstance(message, str):
                response_message = types.ResponseMessage(
                    text=types.ResponseMessage.Text(text=[message])
                )
            elif isinstance(message, list):
                if not all((isinstance(msg, str) for msg in message)):
                    raise ValueError(
                        "Only strings are allowed in message list."
                    )
                response_message = types.ResponseMessage(
                    text=types.ResponseMessage.Text(text=message)
                )
            else:
                raise ValueError(
                    "For 'text' message should be"
                    " either a string or a list of strings."
                )
        elif response_type == "live_agent_handoff":
            if isinstance(message, dict):
                if not all((isinstance(key, str) for key in message.keys())):
                    raise ValueError(
                        "Only strings are allowed as dictionary keys in message."
                    )
                proto_struct = struct_pb2.Struct()
                proto_struct.update(message)
                live_agent_handoff = types.ResponseMessage.LiveAgentHandoff(
                    metadata=proto_struct
                )
                response_message = types.ResponseMessage(
                    live_agent_handoff=live_agent_handoff
                )
            else:
                raise ValueError(
                    "For 'live_agent_handoff',"
                    " message should be a dictionary."
                )
            pass
        elif response_type == "conversation_success":
            if isinstance(message, dict):
                if not all((isinstance(key, str) for key in message.keys())):
                    raise ValueError(
                        "Only strings are allowed as dictionary keys in message"
                    )
                proto_struct = struct_pb2.Struct()
                proto_struct.update(message)
                convo_success = types.ResponseMessage.ConversationSuccess(
                    metadata=proto_struct
                )
                response_message = types.ResponseMessage(
                    conversation_success=convo_success
                )
            else:
                raise ValueError(
                    "For 'conversation_success',"
                    " message should be a dictionary."
                )
            pass
        elif response_type == "output_audio_text":
            if isinstance(message, str):
                if mode == "text":
                    output_audio_text = types.ResponseMessage.OutputAudioText(
                        text=message
                    )
                elif mode == "ssml":
                    output_audio_text = types.ResponseMessage.OutputAudioText(
                        ssml=message
                    )
                else:
                    raise ValueError(
                        "mode should be either 'text' or 'ssml'"
                        " for output_audio_text."
                    )
                response_message = types.ResponseMessage(
                    output_audio_text=output_audio_text
                )
            else:
                raise ValueError(
                    "For 'output_audio_text', message should be a string."
                )
        elif response_type == "play_audio":
            if isinstance(message, str):
                # Validate the URI here if needed
                response_message = types.ResponseMessage(
                    play_audio=types.ResponseMessage.PlayAudio(
                        audio_uri=message
                    )
                )
            else:
                raise ValueError(
                    "For 'play_audio', message should be a valid URI."
                )
        elif response_type == "telephony_transfer_call":
            if isinstance(message, str):
                # Validate the E.164 format here if needed
                transfer_call_obj = types.ResponseMessage.TelephonyTransferCall(
                    phone_number=message
                )
                response_message = types.ResponseMessage(
                    telephony_transfer_call=transfer_call_obj
                )
            else:
                raise ValueError(
                    "For 'telephony_transfer_call',"
                    " message should be a valid E.164 format phone number."
                )
        else:
            raise ValueError(
                "response_type should be one of the following:"
                " 'text', 'live_agent_handoff', 'conversation_success',"
                " 'output_audio_text', 'play_audio', 'telephony_transfer_call'"
            )
    

    def add_response_message(
        self,
        response_type: str,
        message: Union[str, List[str], Dict[str, Any]],
        mode: str = None
    ) -> types.Fulfillment:
        """Add a rich message response to present to the user.

        Args:
            response_type (str):
                Type of the response message. It should be one of the following:
                'text', 'live_agent_handoff', 'conversation_success',
                'output_audio_text', 'play_audio', 'telephony_transfer_call'
            message (str | List[str] | Dict[str, str]):
                The output message. For each response_type
                it should be formatted like the following:
                    text --> str | List[str]
                    live_agent_handoff --> Dict[str, Any]
                    conversation_success --> Dict[str, Any]
                    output_audio_text --> str
                    play_audio --> str
                    telephony_transfer_call --> str
            mode (str):
                This argument is only applicable for 'output_audio_text'.
                It should be one of the following: 'text', 'ssml'

        Returns:
            A Fulfillment object stored in proto_obj
        """
        self._check_fulfillment_exist()

        response_msg = self._response_message_creator(
            response_type=response_type, message=message, mode=mode
        )
        self.proto_obj.messages.append(response_msg)

        return self.proto_obj


    def add_parameter_presets(
        self,
        parameter_map: Dict[str, str]
    ) -> types.Fulfillment:
        """Set parameter values. For single 

        Args:
            parameter_map (Dict[str, str]):
                A dictionary that represents parameters as keys
                and the parameter values as it's values.
        Returns:
            A Fulfillment object stored in proto_obj
        """
        self._check_fulfillment_exist()

        if isinstance(parameter_map, dict):
            if not all((
                isinstance(key, str) and isinstance(val, str)
                for key, val in parameter_map.items()
            )):
                raise ValueError(
                    "Only strings are allowed as"
                    " dictionary keys and values in parameter_map."
                ) 
            for parameter, value in parameter_map.items(): 
                self.proto_obj.set_parameter_actions.append(
                    types.Fulfillment.SetParameterAction(
                        parameter=parameter, value=value
                    )
                )

            return self.proto_obj
        else:
            raise ValueError(
                "parameter_map should be a dictionary."
            )


    def create_empty_fulfillment(
        self,
        webhook: str = None,
        tag: str = None,
        return_partial_responses: bool = False,
        overwrite: bool = False
    ) -> types.Fulfillment:
        """Create an empty Fulfillment.

        Args:
            webhook (str):
                The webhook to call. Format:
                ``projects/<Project ID>/locations/<Location ID>/agents
                  /<Agent ID>/webhooks/<Webhook ID>``.
            tag (str):
                The value of this field will be populated in the
                [WebhookRequest][google.cloud.dialogflow.cx.v3beta1.WebhookRequest]
                ``fulfillmentInfo.tag`` field by Dialogflow when the
                associated webhook is called. The tag is typically used by
                the webhook service to identify which fulfillment is being
                called, but it could be used for other purposes. This field
                is required if ``webhook`` is specified.
            return_partial_responses (bool):
                Whether Dialogflow should return currently
                queued fulfillment response messages in
                streaming APIs. If a webhook is specified, it
                happens before Dialogflow invokes webhook.
            overwrite (bool)
                Overwrite the new proto_obj if proto_obj already
                contains a Fulfillment.

        Returns:
            A Fulfillment object stored in proto_obj.
        """
        if (return_partial_responses and
            not isinstance(return_partial_responses, bool)):
            raise ValueError(
                "return_partial_responses should be bool."
            )
        if ((webhook and not isinstance(webhook, str)) or
            (tag and not isinstance(tag, str))):
            raise ValueError(
                "webhook and tag should be string."
            )
        if webhook and not tag:
            raise ValueError(
                "tag is required when webhook is specified."
            )
        if self.proto_obj and not overwrite:
            raise Exception(
                "proto_obj already contains a Fulfillment."
                " If you wish to overwrite it, pass overwrite as True."
            )
        if overwrite or not self.proto_obj:
            self.proto_obj = types.Fulfillment(
                webhook=webhook,
                return_partial_responses=return_partial_responses,
                tag=tag
            )

        return self.proto_obj


    def add_conditional_case(
        self,
    ) -> types.Fulfillment:
        """A list of cascading if-else conditions. Cases are mutually
        exclusive. The first one with a matching condition is selected,
        all the rest ignored.

        Args:

        Returns:
          A Fulfillment object stored in proto_obj
        """
        self._check_fulfillment_exist()



class TransitionRouteBuilder:
    """Base Class for CX TransitionRoute builder."""


    def __init__(self, obj: types.TransitionRoute = None):
        self.proto_obj = None
        if obj:
            self.load_transition_route(obj)


    def _check_transition_route_exist(self):
        """Check if the proto_obj exists otherwise raise an error."""

        if not self.proto_obj:
            raise ValueError(
                "There is no proto_obj!\nUse create_empty_transition_route"
                " or load_transition_route to continue."
            )
        elif not isinstance(self.proto_obj, types.TransitionRoute):
            raise ValueError(
                "proto_obj is not a TransitionRoute type."
                "\nPlease create or load the correct type to continue."
            )


    def load_transition_route(
        self, obj: types.TransitionRoute, overwrite: bool = False
    ) -> types.TransitionRoute:
        """Load an existing TransitionRoute to proto_obj for further uses.

        Args:
          obj (TransitionRoute):
            An existing TransitionRoute obj.
          overwrite (bool)
            Overwrite the new proto_obj if proto_obj already
            contains a TransitionRoute.

        Returns:
          A TransitionRoute object stored in proto_obj
        """
        if not isinstance(obj, types.TransitionRoute):
            raise ValueError(
                "The object you're trying to load is not a TransitionRoute!"
            )
        if self.proto_obj and not overwrite:
            raise Exception(
                "proto_obj already contains a TransitionRoute."
                " If you wish to overwrite it, pass overwrite as True."
            )
        if overwrite or not self.proto_obj:
            self.proto_obj = obj

        return self.proto_obj


    def create_empty_transition_route(
        self,
        intent: str = None,
        condition: str = None,
        trigger_fulfillment: types.Fulfillment = None,
        target_page: str = None,
        target_flow: str = None,
        overwrite: bool = False
    ) -> types.TransitionRoute:
        """Create an empty TransitionRoute.

        Args:
            intent (str):
                Indicates that the transition can only happen when the given
                intent is matched.
                Format:
                ``projects/<Project ID>/locations/<Location ID>/
                  agents/<Agent ID>/intents/<Intent ID>``.
                At least one of ``intent`` or ``condition`` must be specified.
                When both ``intent`` and ``condition`` are specified,
                the transition can only happen when both are fulfilled.
            condition (str):
                The condition to evaluate.
                See the conditions reference:
                https://cloud.google.com/dialogflow/cx/docs/reference/condition
                At least one of ``intent`` or ``condition`` must be specified.
                When both ``intent`` and ``condition`` are specified,
                the transition can only happen when both are fulfilled.
            trigger_fulfillment (Fulfillment):
                The fulfillment to call when the condition is satisfied.
                When ``trigger_fulfillment`` and ``target`` are defined,
                ``trigger_fulfillment`` is executed first.
            target_page (str):
                The target page to transition to. Format:
                ``projects/<Project ID>/locations/<Location ID>/
                  agents/<Agent ID>/flows/<Flow ID>/pages/<Page ID>``.
                At most one of ``target_page`` and ``target_flow``
                can be specified at the same time.
            target_flow (str):
                The target flow to transition to. Format:
                ``projects/<Project ID>/locations/<Location ID>/
                  agents/<Agent ID>/flows/<Flow ID>``.
                At most one of ``target_page`` and ``target_flow``
                can be specified at the same time.
            overwrite (bool)
                Overwrite the new proto_obj if proto_obj already
                contains a TransitionRoute.

        Returns:
            A TransitionRoute object stored in proto_obj.
        """
        if ((intent and not isinstance(intent, str)) or
            (condition and not isinstance(condition, str)) or
            (target_page and not isinstance(target_page, str)) or
            (target_flow and not isinstance(target_flow, str))):
            raise ValueError(
                "intent, condition, target_page, and target_flow"
                " if existed should be a string."
            )
        if (trigger_fulfillment and
            not isinstance(trigger_fulfillment, types.Fulfillment)):
            raise ValueError(
                "trigger_fulfillment type should be a Fulfillment."
            )
        if target_page and target_flow:
            raise Exception(
                "At most one of target_page and target_flow"
                " can be specified at the same time."
            )
        if self.proto_obj and not overwrite:
            raise Exception(
                "proto_obj already contains a TransitionRoute."
                " If you wish to overwrite it, pass overwrite as True."
            )
        if overwrite or not self.proto_obj:
            if not trigger_fulfillment:
                self.proto_obj = types.TransitionRoute(
                    intent=intent,
                    condition=condition,
                    trigger_fulfillment=types.Fulfillment(),
                    target_page=target_page,
                    target_flow=target_flow
                )
            else:
                self.proto_obj = types.TransitionRoute(
                    intent=intent,
                    condition=condition,
                    trigger_fulfillment=trigger_fulfillment,
                    target_page=target_page,
                    target_flow=target_flow
                )

        return self.proto_obj


class EventHandlerBuilder:
    """Base Class for CX EventHandler builder."""


    def __init__(self, obj: types.EventHandler = None):
        self.proto_obj = None
        if obj:
            self.load_event_handler(obj)


    def _check_event_handler_exist(self):
        """Check if the proto_obj exists otherwise raise an error."""

        if not self.proto_obj:
            raise ValueError(
                "There is no proto_obj!\nUse create_empty_event_handler"
                " or load_event_handler to continue."
            )
        elif not isinstance(self.proto_obj, types.EventHandler):
            raise ValueError(
                "proto_obj is not an EventHandler type."
                "\nPlease create or load the correct type to continue."
            )


    def load_event_handler(
        self, obj: types.EventHandler, overwrite: bool = False
    ) -> types.EventHandler:
        """Load an existing EventHandler to proto_obj for further uses.

        Args:
          obj (EventHandler):
            An existing EventHandler obj.
          overwrite (bool)
            Overwrite the new proto_obj if proto_obj already
            contains an EventHandler.

        Returns:
          An EventHandler object stored in proto_obj
        """
        if not isinstance(obj, types.EventHandler):
            raise ValueError(
                "The object you're trying to load is not an EventHandler!"
            )
        if self.proto_obj and not overwrite:
            raise Exception(
                "proto_obj already contains an EventHandler."
                " If you wish to overwrite it, pass overwrite as True."
            )
        if overwrite or not self.proto_obj:
            self.proto_obj = obj

        return self.proto_obj


    def create_empty_event_handler(
        self,
        event: str,
        trigger_fulfillment: types.Fulfillment = None,
        target_page: str = None,
        target_flow: str = None,
        overwrite: bool = False
    ) -> types.EventHandler:
        """Create an empty EventHandler.

        Args:
            event (str):
                Required. The name of the event to handle.
            trigger_fulfillment (Fulfillment):
                The fulfillment to call when the event occurs.
                Handling webhook errors with a fulfillment enabled with webhook
                could cause infinite loop. It is invalid to specify
                such fulfillment for a handler handling webhooks.
            target_page (str):
                The target page to transition to. Format:
                ``projects/<Project ID>/locations/<Location ID>/
                  agents/<Agent ID>/flows/<Flow ID>/pages/<Page ID>``.
                At most one of ``target_page`` and ``target_flow``
                can be specified at the same time.
            target_flow (str):
                The target flow to transition to. Format:
                ``projects/<Project ID>/locations/<Location ID>/
                  agents/<Agent ID>/flows/<Flow ID>``.
                At most one of ``target_page`` and ``target_flow``
                can be specified at the same time.
            overwrite (bool)
                Overwrite the new proto_obj if proto_obj already
                contains a EventHandler.

        Returns:
            An EventHandler object stored in proto_obj.
        """
        if event and not isinstance(event, str):
            raise ValueError("event should be a string.")
        if (trigger_fulfillment and
            not isinstance(trigger_fulfillment, types.Fulfillment)):
            raise ValueError(
                "trigger_fulfillment type should be a Fulfillment."
            )
        if target_page and target_flow:
            raise Exception(
                "At most one of target_page and target_flow"
                " can be specified at the same time."
            )
        if self.proto_obj and not overwrite:
            raise Exception(
                "proto_obj already contains an EventHandler."
                " If you wish to overwrite it, pass overwrite as True."
            )
        if overwrite or not self.proto_obj:
            self.proto_obj = types.EventHandler(
                event=event,
                trigger_fulfillment=trigger_fulfillment,
                target_page=target_page,
                target_flow=target_flow
            )

        return self.proto_obj
