# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import notifySeller_pb2 as notifySeller__pb2


class SellerNotificationStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.NotifySeller = channel.unary_unary(
                '/SellerNotification/NotifySeller',
                request_serializer=notifySeller__pb2.NotifySellerRequest.SerializeToString,
                response_deserializer=notifySeller__pb2.NotifySellerResponse.FromString,
                )


class SellerNotificationServicer(object):
    """Missing associated documentation comment in .proto file."""

    def NotifySeller(self, request, context):
        """Method for market to send notification to the seller
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_SellerNotificationServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'NotifySeller': grpc.unary_unary_rpc_method_handler(
                    servicer.NotifySeller,
                    request_deserializer=notifySeller__pb2.NotifySellerRequest.FromString,
                    response_serializer=notifySeller__pb2.NotifySellerResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'SellerNotification', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class SellerNotification(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def NotifySeller(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/SellerNotification/NotifySeller',
            notifySeller__pb2.NotifySellerRequest.SerializeToString,
            notifySeller__pb2.NotifySellerResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
