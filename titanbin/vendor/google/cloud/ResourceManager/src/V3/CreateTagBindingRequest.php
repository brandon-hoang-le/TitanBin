<?php
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/cloud/resourcemanager/v3/tag_bindings.proto

namespace Google\Cloud\ResourceManager\V3;

use Google\Protobuf\Internal\GPBType;
use Google\Protobuf\Internal\RepeatedField;
use Google\Protobuf\Internal\GPBUtil;

/**
 * The request message to create a TagBinding.
 *
 * Generated from protobuf message <code>google.cloud.resourcemanager.v3.CreateTagBindingRequest</code>
 */
class CreateTagBindingRequest extends \Google\Protobuf\Internal\Message
{
    /**
     * Required. The TagBinding to be created.
     *
     * Generated from protobuf field <code>.google.cloud.resourcemanager.v3.TagBinding tag_binding = 1 [(.google.api.field_behavior) = REQUIRED];</code>
     */
    private $tag_binding = null;
    /**
     * Optional. Set to true to perform the validations necessary for creating the resource,
     * but not actually perform the action.
     *
     * Generated from protobuf field <code>bool validate_only = 2 [(.google.api.field_behavior) = OPTIONAL];</code>
     */
    private $validate_only = false;

    /**
     * Constructor.
     *
     * @param array $data {
     *     Optional. Data for populating the Message object.
     *
     *     @type \Google\Cloud\ResourceManager\V3\TagBinding $tag_binding
     *           Required. The TagBinding to be created.
     *     @type bool $validate_only
     *           Optional. Set to true to perform the validations necessary for creating the resource,
     *           but not actually perform the action.
     * }
     */
    public function __construct($data = NULL) {
        \GPBMetadata\Google\Cloud\Resourcemanager\V3\TagBindings::initOnce();
        parent::__construct($data);
    }

    /**
     * Required. The TagBinding to be created.
     *
     * Generated from protobuf field <code>.google.cloud.resourcemanager.v3.TagBinding tag_binding = 1 [(.google.api.field_behavior) = REQUIRED];</code>
     * @return \Google\Cloud\ResourceManager\V3\TagBinding|null
     */
    public function getTagBinding()
    {
        return isset($this->tag_binding) ? $this->tag_binding : null;
    }

    public function hasTagBinding()
    {
        return isset($this->tag_binding);
    }

    public function clearTagBinding()
    {
        unset($this->tag_binding);
    }

    /**
     * Required. The TagBinding to be created.
     *
     * Generated from protobuf field <code>.google.cloud.resourcemanager.v3.TagBinding tag_binding = 1 [(.google.api.field_behavior) = REQUIRED];</code>
     * @param \Google\Cloud\ResourceManager\V3\TagBinding $var
     * @return $this
     */
    public function setTagBinding($var)
    {
        GPBUtil::checkMessage($var, \Google\Cloud\ResourceManager\V3\TagBinding::class);
        $this->tag_binding = $var;

        return $this;
    }

    /**
     * Optional. Set to true to perform the validations necessary for creating the resource,
     * but not actually perform the action.
     *
     * Generated from protobuf field <code>bool validate_only = 2 [(.google.api.field_behavior) = OPTIONAL];</code>
     * @return bool
     */
    public function getValidateOnly()
    {
        return $this->validate_only;
    }

    /**
     * Optional. Set to true to perform the validations necessary for creating the resource,
     * but not actually perform the action.
     *
     * Generated from protobuf field <code>bool validate_only = 2 [(.google.api.field_behavior) = OPTIONAL];</code>
     * @param bool $var
     * @return $this
     */
    public function setValidateOnly($var)
    {
        GPBUtil::checkBool($var);
        $this->validate_only = $var;

        return $this;
    }

}

