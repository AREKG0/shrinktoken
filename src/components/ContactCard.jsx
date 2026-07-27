import React from 'react'

export default function ContactCard() {
  return (
    <div className="h-[10em] w-[18em] bg-white rounded-[1em] relative group p-5 z-0 overflow-hidden shadow-2xl transition-transform hover:scale-105">
      {/* Animated Colored Circles */}
      <div className="h-[9em] w-[9em] bg-yellow-400 rounded-full absolute bottom-full -left-[4.5em] group-hover:scale-[550%] z-[-1] duration-[400ms]"></div>
      <div className="h-[7em] w-[7em] bg-green-400 rounded-full absolute bottom-full -left-[3.5em] group-hover:scale-[400%] z-[-1] duration-[400ms] delay-50"></div>
      <div className="h-[5em] w-[5em] bg-blue-500 rounded-full absolute bottom-full -left-[2.5em] group-hover:scale-[300%] z-[-1] duration-[400ms] delay-75"></div>

      {/* Content */}
      <div className="z-20 h-full flex flex-col justify-between">
        <div>
          <h1 className="font-bold font-sans text-xl text-gray-900 group-hover:text-white duration-100 tracking-tight">
            Any Suggestions?
          </h1>
          <p className="text-sm text-gray-600 group-hover:text-white/90 duration-100 mt-1 leading-snug">
            For any queries or feedback, feel free to drop us an email.
          </p>
        </div>

        {/* Mailto Link (Replacing the old button) */}
        <a
          href="mailto:openarc.info.contact@gmail.com"
          className="text-sm font-bold text-blue-600 group-hover:text-white duration-100 flex items-center gap-2 w-fit mt-4"
        >
          <span className="relative before:h-[0.16em] before:absolute before:w-full before:content-[''] before:bg-blue-600 group-hover:before:bg-white duration-100 before:-bottom-1 before:left-0">
            openarc.info.contact@gmail.com
          </span>
        </a>
      </div>
    </div>
  )
}
