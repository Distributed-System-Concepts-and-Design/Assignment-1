# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: notifySeller.proto
# Protobuf Python Version: 4.25.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12notifySeller.proto\"\x87\x02\n\x13NotifySellerRequest\x12\x0e\n\x06itemId\x18\x01 \x01(\r\x12\r\n\x05price\x18\x02 \x01(\x01\x12\x13\n\x0bproductName\x18\x03 \x01(\t\x12/\n\x08\x63\x61tegory\x18\x04 \x01(\x0e\x32\x1d.NotifySellerRequest.Category\x12\x13\n\x0b\x64\x65scription\x18\x05 \x01(\t\x12\x19\n\x11quantityRemaining\x18\x06 \x01(\r\x12\x15\n\rsellerAddress\x18\x07 \x01(\t\x12\x0e\n\x06rating\x18\x08 \x01(\x02\"4\n\x08\x43\x61tegory\x12\x0f\n\x0b\x45LECTRONICS\x10\x00\x12\x0b\n\x07\x46\x41SHION\x10\x01\x12\n\n\x06OTHERS\x10\x02\"g\n\x14NotifySellerResponse\x12,\n\x06status\x18\x01 \x01(\x0e\x32\x1c.NotifySellerResponse.Status\"!\n\x06Status\x12\x0b\n\x07SUCCESS\x10\x00\x12\n\n\x06\x46\x41ILED\x10\x01\x32Q\n\x12SellerNotification\x12;\n\x0cNotifySeller\x12\x14.NotifySellerRequest\x1a\x15.NotifySellerResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'notifySeller_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  _globals['_NOTIFYSELLERREQUEST']._serialized_start=23
  _globals['_NOTIFYSELLERREQUEST']._serialized_end=286
  _globals['_NOTIFYSELLERREQUEST_CATEGORY']._serialized_start=234
  _globals['_NOTIFYSELLERREQUEST_CATEGORY']._serialized_end=286
  _globals['_NOTIFYSELLERRESPONSE']._serialized_start=288
  _globals['_NOTIFYSELLERRESPONSE']._serialized_end=391
  _globals['_NOTIFYSELLERRESPONSE_STATUS']._serialized_start=358
  _globals['_NOTIFYSELLERRESPONSE_STATUS']._serialized_end=391
  _globals['_SELLERNOTIFICATION']._serialized_start=393
  _globals['_SELLERNOTIFICATION']._serialized_end=474
# @@protoc_insertion_point(module_scope)
