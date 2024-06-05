import { useRef } from "react"
import Mimi from "@/components/Mimi"

const MimiPage = () => {
  const mimiRef = useRef(null)
  const voiceRef = useRef(null)
  const scriptRef = useRef(null)
  const rateRef = useRef(null)
  const pitchRef = useRef(null)

  const handleFocus = event => {
    console.log("handleFocus")
    event.currentTarget.value = ""
  }

  const handleBlur = event => {
    console.log("handleBlur")
    const min = parseInt(event.currentTarget.getAttribute("min"))
    const max = parseInt(event.currentTarget.getAttribute("max"))
    const value = parseInt(event.currentTarget.value)

    if (value === 0 || Number.isNaN(value)) {
      event.currentTarget.value = "0"
      return
    }
    if (value < min) {
      event.currentTarget.value = `${min.toString()}%`
      return
    }
    if (value > max) {
      event.currentTarget.value = `${max.toString()}%`
      return
    }
    event.currentTarget.value = `${value.toString()}%`
  }

  const handleClick = () => {
    const voice = voiceRef.current.value
    const script = scriptRef.current.value
    // const rate = rateRef.current.value
    // const pitch = pitchRef.current.value
    // mimiRef.current.activeMimi(voice, script, rate, pitch)
    const rate = '0%'
    const pitch = '0%'
    mimiRef.current.activeMimi(voice, script, rate, pitch)

  }

  return (
    <main className="min-h-screen flex flex-col items-center overflow-y-scroll p-10">
      <div>
        <Mimi ref={mimiRef} onPlayAudio={(status) => { }} />
      </div>
      <div className="w-80 space-y-4">
        <div className="flex items-center gap-4">
          <p>Voice: </p>
          <select
            name="voice"
            ref={voiceRef}
            className="border-2 border-white outline-none px-4 py-2 w-full bg-transparent"
            placeholder="Voice"
          >
            <option value="en-US-JennyNeural">Jenny</option>
            <option value="en-US-SaraNeural">Sara</option>
            <option value="en-US-AriaNeural">Aria</option>
            <option value="en-US-AshleyNeural">Ashley</option>
            <option value="en-US-JasonNeural">Jason</option>
            <option value="en-US-CoraNeural">Cora</option>

            {/* <option value="en-GB-RyanNeural">Ryan</option>
            <option value="en-GB-AbbiNeural">Abbi</option> */}
          </select>
        </div>
        <div className="flex items-center gap-4">
          <p>Script: </p>
          <textarea
            name="script"
            ref={scriptRef}
            className="border-2 border-white focus:border-neutral-500 outline-none px-4 py-2 w-full bg-transparent"
          />
        </div>
        {/* Rate */}
        {/* <div className="flex items-center gap-4">
          <p>Rate: </p>
          <input
            type="text"
            name="rate"
            ref={rateRef}
            className="border-2 border-white focus:border-neutral-500 outline-none w-full px-4 py-2 bg-transparent text-right"
            placeholder="Rate"
            min={-100}
            max={100}
            defaultValue={0}
            onFocus={handleFocus}
            onBlur={handleBlur}
          />
        </div> */}
        {/* Pitch */}
        {/* <div className="flex items-center gap-4">
          <p>Pitch: </p>
          <input
            type="text"
            name="pitch"
            ref={pitchRef}
            className="border-2 border-white focus:border-neutral-500 outline-none w-full px-4 py-2 bg-transparent text-right"
            placeholder="Pitch"
            min={-100}
            max={100}
            defaultValue={0}
            onFocus={handleFocus}
            onBlur={handleBlur}
          />
        </div> */}
        <button
          className="border-2 border-white active:border-neutral-500 active:text-neutral-500 px-4 py-2 w-full"
          onClick={handleClick}
        >
          Play
        </button>
      </div>
    </main>
  )
}
export default MimiPage
