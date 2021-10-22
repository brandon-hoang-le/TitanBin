<?php
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/cloud/automl/v1beta1/detection.proto

namespace GPBMetadata\Google\Cloud\Automl\V1Beta1;

class Detection
{
    public static $is_initialized = false;

    public static function initOnce() {
        $pool = \Google\Protobuf\Internal\DescriptorPool::getGeneratedPool();

        if (static::$is_initialized == true) {
          return;
        }
        \GPBMetadata\Google\Cloud\Automl\V1Beta1\Geometry::initOnce();
        \GPBMetadata\Google\Protobuf\Duration::initOnce();
        \GPBMetadata\Google\Api\Annotations::initOnce();
        $pool->internalAddGeneratedFile(
            '
�

+google/cloud/automl/v1beta1/detection.protogoogle.cloud.automl.v1beta1google/protobuf/duration.protogoogle/api/annotations.proto"p
ImageObjectDetectionAnnotation?
bounding_box (2).google.cloud.automl.v1beta1.BoundingPoly
score ("�
VideoObjectTrackingAnnotation
instance_id (	.
time_offset (2.google.protobuf.Duration?
bounding_box (2).google.cloud.automl.v1beta1.BoundingPoly
score ("�
BoundingBoxMetricsEntry
iou_threshold (
mean_average_precision (o
confidence_metrics_entries (2K.google.cloud.automl.v1beta1.BoundingBoxMetricsEntry.ConfidenceMetricsEntryk
ConfidenceMetricsEntry
confidence_threshold (
recall (
	precision (
f1_score ("�
%ImageObjectDetectionEvaluationMetrics$
evaluated_bounding_box_count (Z
bounding_box_metrics_entries (24.google.cloud.automl.v1beta1.BoundingBoxMetricsEntry+
#bounding_box_mean_average_precision ("�
$VideoObjectTrackingEvaluationMetrics
evaluated_frame_count ($
evaluated_bounding_box_count (Z
bounding_box_metrics_entries (24.google.cloud.automl.v1beta1.BoundingBoxMetricsEntry+
#bounding_box_mean_average_precision (B�
com.google.cloud.automl.v1beta1PZAgoogle.golang.org/genproto/googleapis/cloud/automl/v1beta1;automl�Google\\Cloud\\AutoMl\\V1beta1�Google::Cloud::AutoML::V1beta1bproto3'
        , true);

        static::$is_initialized = true;
    }
}

