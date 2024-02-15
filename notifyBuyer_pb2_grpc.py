# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import notifyBuyer_pb2 as notifyBuyer__pb2


class BuyerNotificationStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.NotifyBuyer = channel.unary_unary(
                '/BuyerNotification/NotifyBuyer',
                request_serializer=notifyBuyer__pb2.NotifyBuyerRequest.SerializeToString,
                response_deserializer=notifyBuyer__pb2.NotifyBuyerResponse.FromString,
                )


class BuyerNotificationServicer(object):
    """Missing associated documentation comment in .proto file."""

    def NotifyBuyer(self, request, context):
        """Method for market to send notification to the buyer
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_BuyerNotificationServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'NotifyBuyer': grpc.unary_unary_rpc_method_handler(
                    servicer.NotifyBuyer,
                    request_deserializer=notifyBuyer__pb2.NotifyBuyerRequest.FromString,
                    response_serializer=notifyBuyer__pb2.NotifyBuyerResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'BuyerNotification', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class BuyerNotification(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def NotifyBuyer(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/BuyerNotification/NotifyBuyer',
            notifyBuyer__pb2.NotifyBuyerRequest.SerializeToString,
            notifyBuyer__pb2.NotifyBuyerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
