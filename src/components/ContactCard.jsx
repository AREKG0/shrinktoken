import React from 'react'

export default function ContactCard() {
  return (
    <div className="h-[10em] w-[18em] bg-white rounded-[1em] relative p-5 z-0 overflow-hidden shadow-2xl transition-transform hover:scale-105">
      {/* Permanently Expanded Colored Circles */}
      <div className="h-[9em] w-[9em] bg-yellow-400 rounded-full absolute bottom-full -left-[4.5em] scale-[550%] z-[-1]"></div>
      <div className="h-[7em] w-[7em] bg-green-400 rounded-full absolute bottom-full -left-[3.5em] scale-[400%] z-[-1]"></div>
      <div className="h-[5em] w-[5em] bg-blue-500 rounded-full absolute bottom-full -left-[2.5em] scale-[300%] z-[-1]"></div>

      {/* Content */}
      <div className="z-20 h-full flex flex-col justify-between">
        <div>
          <h1 className="font-bold font-sans text-xl text-white tracking-tight">
            Any Suggestions?
          </h1>
          <p className="text-sm text-white/90 mt-1 leading-snug">
            For any queries or feedback, feel free to drop us an email.
          </p>
        </div>

        {/* Mailto Link */}
        <a
          href="mailto:openarc.info.contact@gmail.com"
          className="text-sm font-bold text-white flex items-center gap-2 w-fit mt-4 relative group"
        >
          <span className="relative before:h-[0.16em] before:absolute before:w-full before:content-[''] before:bg-white before:opacity-50 group-hover:before:opacity-100 transition-opacity before:-bottom-1 before:left-0">
            openarc.info.contact@gmail.com
          </span>
        </a>
      </div>
    </div>
  )
}
