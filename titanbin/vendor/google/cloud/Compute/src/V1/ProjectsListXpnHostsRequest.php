<?php
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/cloud/compute/v1/compute.proto

namespace Google\Cloud\Compute\V1;

use Google\Protobuf\Internal\GPBType;
use Google\Protobuf\Internal\RepeatedField;
use Google\Protobuf\Internal\GPBUtil;

/**
 *
 * Generated from protobuf message <code>google.cloud.compute.v1.ProjectsListXpnHostsRequest</code>
 */
class ProjectsListXpnHostsRequest extends \Google\Protobuf\Internal\Message
{
    /**
     * Optional organization ID managed by Cloud Resource Manager, for which to list shared VPC host projects. If not specified, the organization will be inferred from the project.
     *
     * Generated from protobuf field <code>string organization = 105180467;</code>
     */
    private $organization = null;

    /**
     * Constructor.
     *
     * @param array $data {
     *     Optional. Data for populating the Message object.
     *
     *     @type string $organization
     *           Optional organization ID managed by Cloud Resource Manager, for which to list shared VPC host projects. If not specified, the organization will be inferred from the project.
     * }
     */
    public function __construct($data = NULL) {
        \GPBMetadata\Google\Cloud\Compute\V1\Compute::initOnce();
        parent::__construct($data);
    }

    /**
     * Optional organization ID managed by Cloud Resource Manager, for which to list shared VPC host projects. If not specified, the organization will be inferred from the project.
     *
     * Generated from protobuf field <code>string organization = 105180467;</code>
     * @return string
     */
    public function getOrganization()
    {
        return isset($this->organization) ? $this->organization : '';
    }

    public function hasOrganization()
    {
        return isset($this->organization);
    }

    public function clearOrganization()
    {
        unset($this->organization);
    }

    /**
     * Optional organization ID managed by Cloud Resource Manager, for which to list shared VPC host projects. If not specified, the organization will be inferred from the project.
     *
     * Generated from protobuf field <code>string organization = 105180467;</code>
     * @param string $var
     * @return $this
     */
    public function setOrganization($var)
    {
        GPBUtil::checkString($var, True);
        $this->organization = $var;

        return $this;
    }

}

