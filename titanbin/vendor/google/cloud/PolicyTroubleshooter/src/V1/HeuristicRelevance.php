<?php
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/cloud/policytroubleshooter/v1/explanations.proto

namespace Google\Cloud\PolicyTroubleshooter\V1;

use UnexpectedValueException;

/**
 * The extent to which a single data point contributes to an overall
 * determination.
 *
 * Protobuf type <code>google.cloud.policytroubleshooter.v1.HeuristicRelevance</code>
 */
class HeuristicRelevance
{
    /**
     * Reserved for future use.
     *
     * Generated from protobuf enum <code>HEURISTIC_RELEVANCE_UNSPECIFIED = 0;</code>
     */
    const HEURISTIC_RELEVANCE_UNSPECIFIED = 0;
    /**
     * The data point has a limited effect on the result. Changing the data point
     * is unlikely to affect the overall determination.
     *
     * Generated from protobuf enum <code>NORMAL = 1;</code>
     */
    const NORMAL = 1;
    /**
     * The data point has a strong effect on the result. Changing the data point
     * is likely to affect the overall determination.
     *
     * Generated from protobuf enum <code>HIGH = 2;</code>
     */
    const HIGH = 2;

    private static $valueToName = [
        self::HEURISTIC_RELEVANCE_UNSPECIFIED => 'HEURISTIC_RELEVANCE_UNSPECIFIED',
        self::NORMAL => 'NORMAL',
        self::HIGH => 'HIGH',
    ];

    public static function name($value)
    {
        if (!isset(self::$valueToName[$value])) {
            throw new UnexpectedValueException(sprintf(
                    'Enum %s has no name defined for value %s', __CLASS__, $value));
        }
        return self::$valueToName[$value];
    }


    public static function value($name)
    {
        $const = __CLASS__ . '::' . strtoupper($name);
        if (!defined($const)) {
            throw new UnexpectedValueException(sprintf(
                    'Enum %s has no value defined for name %s', __CLASS__, $name));
        }
        return constant($const);
    }
}

