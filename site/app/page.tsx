"use client";

import Image from "next/image";
import { motion } from "framer-motion";
import Nav from "./components/narc/Nav";

const FADE_UP = (delay = 0) => ({
  initial: { opacity: 0, y: 18 },
  animate: { opacity: 1, y: 0 },
  transition: { duration: 0.6, delay, ease: "easeOut" as const },
});

const SECTION_FADE = {
  initial: { opacity: 0, y: 24 },
  whileInView: { opacity: 1, y: 0 },
  viewport: { once: true, margin: "-80px" },
  transition: { duration: 0.6, ease: "easeOut" as const },
};

export default function Home() {
  return (
    <div
      className="min-h-screen"
      style={{
        background: "#020204",
        color: "#ffffff",
        fontFamily: "var(--font-headline)",
      }}
    >
      <Nav />

      {/* ── HERO ─────────────────────────────────────────────────── */}
      <section className="flex flex-col items-center text-center px-8 pt-40 pb-32">
        {/* Icon — the centrepiece */}
        <motion.div {...FADE_UP(0)} className="mb-10">
          <Image
            src="/icon.png"
            alt="HydrationNarc app icon"
            width={128}
            height={128}
            priority
            style={{
              borderRadius: "28px",
              boxShadow:
                "0 0 0 1px rgba(255,255,255,0.08), 0 24px 60px rgba(0,0,0,0.7), 0 0 40px rgba(204,255,0,0.08)",
            }}
          />
        </motion.div>

        <motion.p
          {...FADE_UP(0.08)}
          className="text-[11px] font-bold tracking-widest uppercase mb-5"
          style={{ fontFamily: "var(--font-mono)", color: "#CCFF00" }}
        >
          macOS · v1.1.0 · Sensor Daemon
        </motion.p>

        <motion.h1
          {...FADE_UP(0.14)}
          className="font-black leading-[0.92] tracking-tighter mb-6"
          style={{ fontSize: "clamp(44px, 7vw, 96px)", maxWidth: "800px" }}
        >
          Drink water.
          <br />
          Or I&apos;m telling
          <br />
          your kidneys.
        </motion.h1>

        <motion.p
          {...FADE_UP(0.2)}
          className="text-[17px] leading-relaxed mb-10"
          style={{ color: "#71717a", maxWidth: "480px" }}
        >
          A wildly overengineered macOS sensor daemon that tracks your hydration
          using your laptop&apos;s accelerometer. Five algorithms. One verdict.
          No mercy.
        </motion.p>

        <motion.div
          {...FADE_UP(0.26)}
          className="flex flex-wrap items-center justify-center gap-4 mb-16"
        >
          <a
            href="https://buy.stripe.com/6oU7sNgyCelP7B2809fEk00"
            target="_blank"
            rel="noopener noreferrer"
            className="px-8 py-3.5 text-[15px] font-black tracking-tight transition-all duration-150 active:scale-95 hover:brightness-110"
            style={{
              background: "#CCFF00",
              color: "#020204",
              borderRadius: "12px",
              boxShadow: "0 4px 24px rgba(204,255,0,0.22)",
            }}
          >
            Start the Audit — $15
          </a>
          <a
            href="#how-it-works"
            className="px-8 py-3.5 text-[15px] font-black tracking-tight transition-all duration-150 hover:border-white/20"
            style={{
              borderRadius: "12px",
              border: "1px solid rgba(255,255,255,0.1)",
              color: "#71717a",
            }}
          >
            How It Works
          </a>
        </motion.div>

        {/* Stats row */}
        <motion.div
          {...FADE_UP(0.32)}
          className="flex flex-wrap items-center justify-center gap-10"
          style={{ borderTop: "1px solid rgba(255,255,255,0.06)", paddingTop: "32px" }}
        >
          {[
            { value: "2.8M", label: "Sips Audited" },
            { value: "94.1%", label: "Detection Accuracy" },
            { value: "$15", label: "One Time. Forever." },
          ].map(({ value, label }) => (
            <div key={label} className="text-center">
              <p
                className="text-[28px] font-black tracking-tight"
                style={{ color: "#CCFF00" }}
              >
                {value}
              </p>
              <p
                className="text-[11px] font-semibold tracking-widest uppercase mt-1"
                style={{ fontFamily: "var(--font-mono)", color: "#3f3f46" }}
              >
                {label}
              </p>
            </div>
          ))}
        </motion.div>
      </section>

      {/* ── HOW IT WORKS ─────────────────────────────────────────── */}
      <section
        id="how-it-works"
        className="max-w-screen-lg mx-auto px-8 py-28"
        style={{ borderTop: "1px solid rgba(255,255,255,0.06)" }}
      >
        <motion.div {...SECTION_FADE} className="text-center mb-20">
          <p
            className="text-[11px] font-bold tracking-widest uppercase mb-4"
            style={{ fontFamily: "var(--font-mono)", color: "#3f3f46" }}
          >
            How It Works
          </p>
          <h2
            className="font-black tracking-tighter"
            style={{ fontSize: "clamp(28px, 4vw, 52px)" }}
          >
            It watches. You drink.
            <br />
            <span style={{ color: "#CCFF00" }}>Or it tells someone.</span>
          </h2>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {[
            {
              step: "01",
              title: "Sensor Fusion",
              body: "HydrationNarc reads your MacBook's built-in accelerometer and gyroscope at 100 Hz. All processing is local — no microphone, no camera, no cloud.",
              img: "/ghibli-craftsman.png",
              imgAlt: "Craftsman at work",
            },
            {
              step: "02",
              title: "Five-Algorithm Vote",
              body: "High-Pass Filter, CUSUM, Hidden Markov Model, Kalman Smoother, and a 47-tree Random Forest all independently vote. 3/5 minimum for confirmation.",
              img: "/ghibli-waterfall.png",
              imgAlt: "Mountain waterfall",
            },
            {
              step: "03",
              title: "Accountability",
              body: "Miss your target? It notices. Menu bar sip counter, hourly nudges, and a local log of every time you chose dehydration over dignity.",
              img: "/ghibli-map.png",
              imgAlt: "Journey map",
            },
            {
              step: "04",
              title: "Privacy First",
              body: "HydrationNarc is 100% local. No cloud, no telemetry, no tracking. Your hydration data (and your dignity) stay on your machine.",
              img: "/ghibli-hero.png",
              imgAlt: "Privacy and focus",
            },
          ].map(({ step, title, body, img, imgAlt }, i) => (
            <motion.div
              key={step}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-60px" }}
              transition={{ duration: 0.5, delay: i * 0.1, ease: "easeOut" }}
              className="overflow-hidden"
              style={{
                background: "rgba(255,255,255,0.02)",
                border: "1px solid rgba(255,255,255,0.07)",
                borderRadius: "16px",
              }}
            >
              {/* Card image */}
              <div style={{ position: "relative", width: "100%", height: "180px", overflow: "hidden" }}>
                <Image
                  src={img}
                  alt={imgAlt}
                  fill
                  style={{ objectFit: "cover", opacity: 0.75 }}
                  sizes="(max-width: 768px) 100vw, 33vw"
                />
                <div
                  style={{
                    position: "absolute",
                    inset: 0,
                    background: "linear-gradient(to bottom, transparent 40%, rgba(2,2,4,0.95) 100%)",
                  }}
                />
              </div>
              <div className="p-8">
                <p
                  className="text-[11px] font-bold tracking-widest uppercase mb-5"
                  style={{ fontFamily: "var(--font-mono)", color: "#CCFF00" }}
                >
                  {step}
                </p>
                <h3 className="text-[20px] font-black tracking-tight mb-3">
                  {title}
                </h3>
                <p
                  className="text-[14px] leading-relaxed"
                  style={{ color: "#71717a" }}
                >
                  {body}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </section>

      {/* ── THE NERDY BIT ────────────────────────────────────────── */}
      <section
        className="max-w-screen-lg mx-auto px-8 py-28"
        style={{ borderTop: "1px solid rgba(255,255,255,0.06)" }}
      >
        <motion.div
          {...SECTION_FADE}
          className="mx-auto"
          style={{ maxWidth: "640px" }}
        >
          <p
            className="text-[11px] font-bold tracking-widest uppercase mb-4"
            style={{ fontFamily: "var(--font-mono)", color: "#3f3f46" }}
          >
            For the Nerds
          </p>
          <h2
            className="font-black tracking-tighter mb-12"
            style={{ fontSize: "clamp(28px, 4vw, 48px)" }}
          >
            Overengineered by design.
          </h2>

          <div
            className="p-8"
            style={{
              background: "#080809",
              border: "1px solid rgba(255,255,255,0.08)",
              borderRadius: "16px",
            }}
          >
            <p
              className="text-[11px] font-bold tracking-widest uppercase mb-6"
              style={{ fontFamily: "var(--font-mono)", color: "#3f3f46" }}
            >
              voting_engine.swift — 5 algorithms, 1 verdict
            </p>

            <ol className="space-y-5">
              {[
                {
                  n: "01",
                  name: "High-Pass Filter",
                  desc: "4th-order Butterworth, 2 Hz cutoff. Kills gravity drift.",
                },
                {
                  n: "02",
                  name: "CUSUM Detector",
                  desc: "Cumulative sum — catches sustained directional shifts.",
                },
                {
                  n: "03",
                  name: "Hidden Markov Model",
                  desc: "6 states: REST → LIFT → TILT → DRINK → LOWER → RESET.",
                },
                {
                  n: "04",
                  name: "Kalman Smoother",
                  desc: "Pre-processor. Fuses accel + gyro into clean pitch angle.",
                },
                {
                  n: "05",
                  name: "Peak Classifier",
                  desc: "47-tree random forest on 12 hand-engineered features.",
                },
              ].map(({ n, name, desc }) => (
                <li
                  key={n}
                  className="flex gap-5 items-start"
                >
                  <span
                    className="text-[12px] font-bold shrink-0 mt-0.5"
                    style={{ fontFamily: "var(--font-mono)", color: "#3f3f46" }}
                  >
                    {n}
                  </span>
                  <div>
                    <p
                      className="text-[13px] font-bold mb-0.5"
                      style={{ fontFamily: "var(--font-mono)", color: "#e4e4e7" }}
                    >
                      {name}
                    </p>
                    <p
                      className="text-[12px]"
                      style={{ fontFamily: "var(--font-mono)", color: "#52525b" }}
                    >
                      {desc}
                    </p>
                  </div>
                </li>
              ))}
            </ol>

            <div
              className="mt-8 pt-6 flex items-center justify-between"
              style={{ borderTop: "1px solid rgba(255,255,255,0.06)" }}
            >
              <span
                className="text-[11px]"
                style={{ fontFamily: "var(--font-mono)", color: "#3f3f46" }}
              >
                requires 3/5 to confirm a sip
              </span>
              <span
                className="text-[12px] font-black px-3 py-1"
                style={{
                  fontFamily: "var(--font-mono)",
                  background: "rgba(204,255,0,0.08)",
                  color: "#CCFF00",
                  borderRadius: "6px",
                  border: "1px solid rgba(204,255,0,0.15)",
                }}
              >
                SIP CONFIRMED ✓
              </span>
            </div>
          </div>


        </motion.div>
      </section>

      {/* ── PHILOSOPHY STRIP ─────────────────────────────────────── */}
      <motion.section
        {...SECTION_FADE}
        className="py-20 text-center px-8"
        style={{ borderTop: "1px solid rgba(255,255,255,0.06)" }}
      >
        <p
          className="font-black tracking-tighter"
          style={{
            fontSize: "clamp(20px, 3vw, 36px)",
            color: "rgba(255,255,255,0.15)",
            maxWidth: "800px",
            margin: "0 auto",
          }}
        >
          &ldquo;Overengineered so you{" "}
          <span style={{ color: "#ffffff" }}>don&apos;t have to think.</span>
          &rdquo;
        </p>
      </motion.section>

      {/* ── PRICING ──────────────────────────────────────────────── */}
      <section
        id="pricing"
        className="py-32 px-8"
        style={{ borderTop: "1px solid rgba(255,255,255,0.06)" }}
      >
        <motion.div
          {...SECTION_FADE}
          className="mx-auto"
          style={{ maxWidth: "480px" }}
        >
          {/* White card */}
          <div
            className="p-10 mb-6"
            style={{
              background: "#ffffff",
              color: "#020204",
              borderRadius: "20px",
            }}
          >
            <div className="flex items-center gap-4 mb-8">
              <Image
                src="/icon.png"
                alt=""
                width={52}
                height={52}
                style={{ borderRadius: "12px" }}
              />
              <div>
                <p className="text-[18px] font-black tracking-tight">
                  HydrationNarc
                </p>
                <p
                  className="text-[12px]"
                  style={{ fontFamily: "var(--font-mono)", color: "#71717a" }}
                >
                  macOS 12+ · v1.1.0
                </p>
              </div>
            </div>

            <p
              className="font-black tracking-tighter leading-none mb-1"
              style={{ fontSize: "72px" }}
            >
              $15
            </p>
            <p
              className="text-[14px] mb-8"
              style={{ color: "#52525b" }}
            >
              One time. Lifetime access. No subscriptions. No mercy.
            </p>

            <ul className="space-y-2.5 mb-8">
              {[
                "Native accelerometer + gyroscope integration",
                "Five-algorithm voting engine",
                "Local-only data — zero cloud, zero telemetry",
                "Menu bar live sip counter",
                "Configurable hydration targets",
                "Lifetime updates",
              ].map((feat) => (
                <li
                  key={feat}
                  className="flex items-center gap-3 text-[13px]"
                  style={{ color: "#27272a" }}
                >
                  <span
                    style={{
                      width: "16px",
                      height: "16px",
                      borderRadius: "50%",
                      background: "#020204",
                      color: "#CCFF00",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      fontSize: "9px",
                      fontWeight: 900,
                      flexShrink: 0,
                    }}
                  >
                    ✓
                  </span>
                  {feat}
                </li>
              ))}
            </ul>

            <a
              href="https://buy.stripe.com/6oU7sNgyCelP7B2809fEk00"
              target="_blank"
              rel="noopener noreferrer"
              className="block w-full py-4 text-center text-[15px] font-black tracking-tight transition-opacity duration-150 hover:opacity-85 active:opacity-70"
              style={{
                background: "#020204",
                color: "#CCFF00",
                borderRadius: "12px",
              }}
            >
              Start the Audit — $15
            </a>
          </div>

          <p
            className="text-center text-[11px]"
            style={{ fontFamily: "var(--font-mono)", color: "#3f3f46" }}
          >
            macOS only. Your kidneys approve this message.
          </p>
        </motion.div>
      </section>

      {/* ── FOOTER ───────────────────────────────────────────────── */}
      <footer
        className="max-w-screen-lg mx-auto px-8 py-12 flex flex-col md:flex-row items-center justify-between gap-6"
        style={{ borderTop: "1px solid rgba(255,255,255,0.06)" }}
      >
        <div className="flex items-center gap-2.5">
          <Image
            src="/icon.png"
            alt=""
            width={18}
            height={18}
            style={{ borderRadius: "4px", opacity: 0.5 }}
          />
          <span
            className="text-[12px] font-black tracking-tight"
            style={{ color: "#3f3f46" }}
          >
            Hydration<span style={{ color: "#52525b" }}>Narc</span>
          </span>
        </div>

        <div className="flex items-center gap-6">
          <a
            href="https://github.com/Lameda12/hydration-narc"
            className="footer-link text-[11px] font-semibold tracking-widest uppercase"
            style={{ fontFamily: "var(--font-mono)" }}
          >
            GitHub
          </a>
        </div>

        <p
          className="text-[11px]"
          style={{ fontFamily: "var(--font-mono)", color: "#3f3f46" }}
        >
          © {new Date().getFullYear()} HydrationNarc
        </p>
      </footer>
    </div>
  );
}
