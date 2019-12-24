# coding: utf-8

"""
    localhost:8088

    No description provided (generated by Swagger Codegen https://github.com/swagger-api/swagger-codegen)  # noqa: E501

    OpenAPI spec version: 4.0.2
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


import pprint
import re  # noqa: F401

import six


class Endpoint(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'channel_ids': 'list[str]',
        'resource': 'str',
        'state': 'str',
        'technology': 'str'
    }

    attribute_map = {
        'channel_ids': 'channel_ids',
        'resource': 'resource',
        'state': 'state',
        'technology': 'technology'
    }

    def __init__(self, channel_ids=None, resource=None, state=None, technology=None):  # noqa: E501
        """Endpoint - a model defined in Swagger"""  # noqa: E501

        self._channel_ids = None
        self._resource = None
        self._state = None
        self._technology = None
        self.discriminator = None

        self.channel_ids = channel_ids
        self.resource = resource
        if state is not None:
            self.state = state
        self.technology = technology

    @property
    def channel_ids(self):
        """Gets the channel_ids of this Endpoint.  # noqa: E501

        Id's of channels associated with this endpoint  # noqa: E501

        :return: The channel_ids of this Endpoint.  # noqa: E501
        :rtype: list[str]
        """
        return self._channel_ids

    @channel_ids.setter
    def channel_ids(self, channel_ids):
        """Sets the channel_ids of this Endpoint.

        Id's of channels associated with this endpoint  # noqa: E501

        :param channel_ids: The channel_ids of this Endpoint.  # noqa: E501
        :type: list[str]
        """
        if channel_ids is None:
            raise ValueError("Invalid value for `channel_ids`, must not be `None`")  # noqa: E501

        self._channel_ids = channel_ids

    @property
    def resource(self):
        """Gets the resource of this Endpoint.  # noqa: E501

        Identifier of the endpoint, specific to the given technology.  # noqa: E501

        :return: The resource of this Endpoint.  # noqa: E501
        :rtype: str
        """
        return self._resource

    @resource.setter
    def resource(self, resource):
        """Sets the resource of this Endpoint.

        Identifier of the endpoint, specific to the given technology.  # noqa: E501

        :param resource: The resource of this Endpoint.  # noqa: E501
        :type: str
        """
        if resource is None:
            raise ValueError("Invalid value for `resource`, must not be `None`")  # noqa: E501

        self._resource = resource

    @property
    def state(self):
        """Gets the state of this Endpoint.  # noqa: E501

        Endpoint's state  # noqa: E501

        :return: The state of this Endpoint.  # noqa: E501
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """Sets the state of this Endpoint.

        Endpoint's state  # noqa: E501

        :param state: The state of this Endpoint.  # noqa: E501
        :type: str
        """

        self._state = state

    @property
    def technology(self):
        """Gets the technology of this Endpoint.  # noqa: E501

        Technology of the endpoint  # noqa: E501

        :return: The technology of this Endpoint.  # noqa: E501
        :rtype: str
        """
        return self._technology

    @technology.setter
    def technology(self, technology):
        """Sets the technology of this Endpoint.

        Technology of the endpoint  # noqa: E501

        :param technology: The technology of this Endpoint.  # noqa: E501
        :type: str
        """
        if technology is None:
            raise ValueError("Invalid value for `technology`, must not be `None`")  # noqa: E501

        self._technology = technology

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Endpoint, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Endpoint):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other