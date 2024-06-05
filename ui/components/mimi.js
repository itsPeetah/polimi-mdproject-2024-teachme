import { forwardRef, useEffect, useImperativeHandle, useRef } from "react"
import Script from "next/script"
import * as SpeechSDK from "microsoft-cognitiveservices-speech-sdk"
const Mimi = (props, ref) => {
    const { onPlayAudio } = props
    // API Key and Region
    const SPEECH_KEY = process.env.NEXT_PUBLIC_SPEECH_KEY
    const SPEECH_REGION = process.env.NEXT_PUBLIC_SPEECH_REGION
    // Refrences
    const canvasRef = useRef(null)
    // Image Cache
    const imageCache = new Map()
    // Audio
    let ttsAudio
    // Expose function to parent component
    useImperativeHandle(ref, () => ({
        activeMimi(voice, script, rate, pitch) {
            if (voice === "" || script === "") {
                return
            }
            speakMimi(voice, script, rate, pitch)
        }
    }))

    const speakMimi = (voice, script, rate, pitch) => {
        // Synthesizer
        const audioDestination = new SpeechSDK.SpeakerAudioDestination()
        const speechConfig = SpeechSDK.SpeechConfig.fromSubscription(SPEECH_KEY, SPEECH_REGION)
        const audioConfig = SpeechSDK.AudioConfig.fromSpeakerOutput(audioDestination)
        let synthesizer = new SpeechSDK.SpeechSynthesizer(speechConfig, audioConfig)

        audioDestination.onAudioStart = () => {
            audioDestination.pause()
        }
        // Viseme
        let visemes = []
        // SSML
        const ssml = `
      <speak version='1.0' xml:lang='en-US'>
        <voice xml:lang='en-US' name='${voice}' rate='${rate}' pitch='${pitch}'>
          ${script}
        </voice>
      </speak>
    `
        synthesizer.speakSsmlAsync(
            ssml,
            result => {

                if (
                    result.reason ===
                    SpeechSDK.ResultReason.SynthesizingAudioCompleted
                ) {
                    result_SynthesizingAudioCompleted(result.audioData, visemes)
                }

                synthesizer.close()
                synthesizer = undefined
            },
            error => {
                error_SynthesizingAudioCompleted(error)

                synthesizer.close()
                synthesizer = undefined
            }
        )

        // Viseme 
        synthesizer.visemeReceived = (s, e) => {
            // window.console.log("(Viseme), Audio offset: " + e.audioOffset / 10000 + "ms. Viseme ID: " + e.visemeId);

            // `Animation` is an xml string for SVG or a json string for blend shapes
            const animation = e.Animation

            const viseme = {
                offset: e.audioOffset / 10000,
                id: e.visemeId
            }
            visemes.push(viseme)
        }
    }

    const result_SynthesizingAudioCompleted = (audioData, visemes) => {
        const audioUrl = URL.createObjectURL(
            new Blob([audioData], { type: "audio/mp3" })
        )
        playAudio(audioUrl, visemes)
    }

    const error_SynthesizingAudioCompleted = error => {
        console.log(error)
    }

    const loadImageBySrc = pathname => {
        if (imageCache.has(pathname)) {
            return Promise.resolve(imageCache.get(pathname))
        }

        return new Promise(resolve => {
            const image = new Image()
            image.onload = () => {
                imageCache.set(pathname, image)
                resolve(image)
            }
            image.src = pathname
        })
    }

    const drawImage = async pathname => {
        const image = await loadImageBySrc(pathname)
        try {
            canvasRef.current.getContext("2d").drawImage(image, 0, 0)
        } catch (e) { }
    }

    const clearEyes = () => {
        try {
            canvasRef.current.getContext("2d").fillStyle = "rgb(90, 81, 74)"
            canvasRef.current.getContext("2d").fillRect(89, 86, 40, 44)
            canvasRef.current.getContext("2d").fillRect(175, 86, 40, 44)
        } catch (e) { }
    }

    const sleep = ms => {
        return new Promise(resolve => setTimeout(resolve, ms))
    }

    const eyeBlink = async () => {
        try {
            const leftEye = await loadImageBySrc("/mimi/images/eye-l.png")
            const rightEye = await loadImageBySrc("/mimi/images/eye-r.png")

            const targetHeight = Math.floor(leftEye.height * 0.2)
            const ANIMATION_STEP = 20
            let height = leftEye.height

            while (height > targetHeight) {
                await sleep(ANIMATION_STEP)
                height *= 0.8
                clearEyes()
                canvasRef.current
                    .getContext("2d")
                    .drawImage(
                        leftEye,
                        0,
                        (leftEye.height - height) / 3,
                        leftEye.width,
                        height
                    )
                canvasRef.current
                    .getContext("2d")
                    .drawImage(
                        rightEye,
                        0,
                        (rightEye.height - height) / 3,
                        rightEye.width,
                        height
                    )
            }

            await sleep(ANIMATION_STEP)
            clearEyes()
            canvasRef.current
                .getContext("2d")
                .drawImage(
                    leftEye,
                    0,
                    (leftEye.height - targetHeight) / 3,
                    leftEye.width,
                    targetHeight
                )
            canvasRef.current
                .getContext("2d")
                .drawImage(
                    rightEye,
                    0,
                    (rightEye.height - targetHeight) / 3,
                    rightEye.width,
                    targetHeight
                )

            await sleep(75)
            clearEyes()
            await drawImage("/mimi/images/eye-l-closed.png")
            await drawImage("/mimi/images/eye-r-closed.png")

            await sleep(120)
            clearEyes()
            await drawImage("/mimi/images/eye-l.png")
            await drawImage("/mimi/images/eye-r.png")
        } catch { }
    }

    const drawMouthFrame = async id => {
        const image = await loadImageBySrc(`/mimi/images/mouth-${id}.png`)
        try {
            canvasRef.current.getContext("2d").fillStyle = "rgb(90, 81, 74)"
            canvasRef.current.getContext("2d").fillRect(100, 75, 1, 1)
            canvasRef.current.getContext("2d").drawImage(image, 0, 0)
        } catch { }
    }

    const playAudio = async (audioUrl, visemes) => {
        if (ttsAudio) {
            ttsAudio.pause()
        }
        ttsAudio = new Audio(audioUrl)

        ttsAudio.ontimeupdate = () => {
            const TRANSITION_DELAY = 60
            const currentViseme = visemes.find(viseme => {
                return (
                    viseme.offset - TRANSITION_DELAY / 2 >= ttsAudio.currentTime * 1000
                )
            })

            if (currentViseme) {
                drawMouthFrame(currentViseme.id ?? 0)
            }
        }

        ttsAudio.play()
        // Notify parent component that audio is playing
        onPlayAudio(true)
        await new Promise((resolve) => {
            ttsAudio.addEventListener('ended', resolve);
        });
        // Notify parent component that audio has finished playing
        onPlayAudio(false)
    }

    useEffect(() => {
        const drawMimi = async () => {
            const imageIds = [
                "/mimi/images/body.png",
                "/mimi/images/eye-l.png",
                "/mimi/images/eye-r.png",
                "/mimi/images/mouth-0.png"
            ]
            imageIds.forEach(async imageId => {
                const image = await loadImageBySrc(imageId)
                try {
                    canvasRef.current.getContext("2d").drawImage(image, 0, 0)
                } catch { }
            })

            const BLINK_INTERVAL = 3500
            setInterval(() => {
                eyeBlink()
            }, BLINK_INTERVAL)
        }
        drawMimi().catch(e => {
            // handle the error as needed
            console.error("An error occurred while fetching the data: ", e)
        })
    }, [])

    return (
        <>
            <Script src="https://aka.ms/csspeech/jsbrowserpackageraw" />
            <canvas id="canvas" ref={canvasRef} width={312} height={312} />
        </>
    )
}
export default forwardRef(Mimi)
