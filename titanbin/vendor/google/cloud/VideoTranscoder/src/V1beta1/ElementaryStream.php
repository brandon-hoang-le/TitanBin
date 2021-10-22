<?php
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/cloud/video/transcoder/v1beta1/resources.proto

namespace Google\Cloud\Video\Transcoder\V1beta1;

use Google\Protobuf\Internal\GPBType;
use Google\Protobuf\Internal\RepeatedField;
use Google\Protobuf\Internal\GPBUtil;

/**
 * Encoding of an input file such as an audio, video, or text track.
 * Elementary streams must be packaged before
 * mapping and sharing between different output formats.
 *
 * Generated from protobuf message <code>google.cloud.video.transcoder.v1beta1.ElementaryStream</code>
 */
class ElementaryStream extends \Google\Protobuf\Internal\Message
{
    /**
     * A unique key for this elementary stream.
     *
     * Generated from protobuf field <code>string key = 4;</code>
     */
    private $key = '';
    protected $elementary_stream;

    /**
     * Constructor.
     *
     * @param array $data {
     *     Optional. Data for populating the Message object.
     *
     *     @type string $key
     *           A unique key for this elementary stream.
     *     @type \Google\Cloud\Video\Transcoder\V1beta1\VideoStream $video_stream
     *           Encoding of a video stream.
     *     @type \Google\Cloud\Video\Transcoder\V1beta1\AudioStream $audio_stream
     *           Encoding of an audio stream.
     *     @type \Google\Cloud\Video\Transcoder\V1beta1\TextStream $text_stream
     *           Encoding of a text stream. For example, closed captions or subtitles.
     * }
     */
    public function __construct($data = NULL) {
        \GPBMetadata\Google\Cloud\Video\Transcoder\V1Beta1\Resources::initOnce();
        parent::__construct($data);
    }

    /**
     * A unique key for this elementary stream.
     *
     * Generated from protobuf field <code>string key = 4;</code>
     * @return string
     */
    public function getKey()
    {
        return $this->key;
    }

    /**
     * A unique key for this elementary stream.
     *
     * Generated from protobuf field <code>string key = 4;</code>
     * @param string $var
     * @return $this
     */
    public function setKey($var)
    {
        GPBUtil::checkString($var, True);
        $this->key = $var;

        return $this;
    }

    /**
     * Encoding of a video stream.
     *
     * Generated from protobuf field <code>.google.cloud.video.transcoder.v1beta1.VideoStream video_stream = 1;</code>
     * @return \Google\Cloud\Video\Transcoder\V1beta1\VideoStream|null
     */
    public function getVideoStream()
    {
        return $this->readOneof(1);
    }

    public function hasVideoStream()
    {
        return $this->hasOneof(1);
    }

    /**
     * Encoding of a video stream.
     *
     * Generated from protobuf field <code>.google.cloud.video.transcoder.v1beta1.VideoStream video_stream = 1;</code>
     * @param \Google\Cloud\Video\Transcoder\V1beta1\VideoStream $var
     * @return $this
     */
    public function setVideoStream($var)
    {
        GPBUtil::checkMessage($var, \Google\Cloud\Video\Transcoder\V1beta1\VideoStream::class);
        $this->writeOneof(1, $var);

        return $this;
    }

    /**
     * Encoding of an audio stream.
     *
     * Generated from protobuf field <code>.google.cloud.video.transcoder.v1beta1.AudioStream audio_stream = 2;</code>
     * @return \Google\Cloud\Video\Transcoder\V1beta1\AudioStream|null
     */
    public function getAudioStream()
    {
        return $this->readOneof(2);
    }

    public function hasAudioStream()
    {
        return $this->hasOneof(2);
    }

    /**
     * Encoding of an audio stream.
     *
     * Generated from protobuf field <code>.google.cloud.video.transcoder.v1beta1.AudioStream audio_stream = 2;</code>
     * @param \Google\Cloud\Video\Transcoder\V1beta1\AudioStream $var
     * @return $this
     */
    public function setAudioStream($var)
    {
        GPBUtil::checkMessage($var, \Google\Cloud\Video\Transcoder\V1beta1\AudioStream::class);
        $this->writeOneof(2, $var);

        return $this;
    }

    /**
     * Encoding of a text stream. For example, closed captions or subtitles.
     *
     * Generated from protobuf field <code>.google.cloud.video.transcoder.v1beta1.TextStream text_stream = 3;</code>
     * @return \Google\Cloud\Video\Transcoder\V1beta1\TextStream|null
     */
    public function getTextStream()
    {
        return $this->readOneof(3);
    }

    public function hasTextStream()
    {
        return $this->hasOneof(3);
    }

    /**
     * Encoding of a text stream. For example, closed captions or subtitles.
     *
     * Generated from protobuf field <code>.google.cloud.video.transcoder.v1beta1.TextStream text_stream = 3;</code>
     * @param \Google\Cloud\Video\Transcoder\V1beta1\TextStream $var
     * @return $this
     */
    public function setTextStream($var)
    {
        GPBUtil::checkMessage($var, \Google\Cloud\Video\Transcoder\V1beta1\TextStream::class);
        $this->writeOneof(3, $var);

        return $this;
    }

    /**
     * @return string
     */
    public function getElementaryStream()
    {
        return $this->whichOneof("elementary_stream");
    }

}

