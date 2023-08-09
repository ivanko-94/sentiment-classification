# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from generated import text_classification_service_pb2 as generated_dot_text__classification__service__pb2


class TextClassificationServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Classify = channel.unary_unary(
                '/text.classification.proto.grpc.TextClassificationService/Classify',
                request_serializer=generated_dot_text__classification__service__pb2.InputText.SerializeToString,
                response_deserializer=generated_dot_text__classification__service__pb2.Prediction.FromString,
                )


class TextClassificationServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Classify(self, request, context):
        """classifies string and returns a class name as a response
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_TextClassificationServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Classify': grpc.unary_unary_rpc_method_handler(
                    servicer.Classify,
                    request_deserializer=generated_dot_text__classification__service__pb2.InputText.FromString,
                    response_serializer=generated_dot_text__classification__service__pb2.Prediction.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'text.classification.proto.grpc.TextClassificationService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class TextClassificationService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Classify(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/text.classification.proto.grpc.TextClassificationService/Classify',
            generated_dot_text__classification__service__pb2.InputText.SerializeToString,
            generated_dot_text__classification__service__pb2.Prediction.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
