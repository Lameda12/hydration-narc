import Link from "next/link";
import Image from "next/image";

export default function Nav() {
  return (
    <header
      className="fixed top-0 inset-x-0 z-50 flex items-center justify-between px-8 py-5"
      style={{
        background: "rgba(2,2,4,0.85)",
        backdropFilter: "blur(20px)",
        WebkitBackdropFilter: "blur(20px)",
        borderBottom: "1px solid rgba(255,255,255,0.06)",
      }}
    >
      <Link href="/" className="flex items-center gap-2.5">
        <Image
          src="/icon.png"
          alt="HydrationNarc"
          width={22}
          height={22}
          style={{ borderRadius: "6px" }}
        />
        <span
          className="text-[15px] font-black tracking-tight"
          style={{ fontFamily: "var(--font-headline)" }}
        >
          Hydration<span style={{ color: "#CCFF00" }}>Narc</span>
        </span>
      </Link>

      <a
        href="https://buy.stripe.com/6oU7sNgyCelP7B2809fEk00"
        target="_blank"
        rel="noopener noreferrer"
        className="px-5 py-2.5 text-[13px] font-black tracking-tight transition-all duration-150 active:scale-95 hover:brightness-110"
        style={{
          background: "#CCFF00",
          color: "#020204",
          borderRadius: "10px",
          fontFamily: "var(--font-headline)",
          boxShadow: "0 2px 14px rgba(204,255,0,0.18)",
        }}
      >
        Buy — $15
      </a>
    </header>
  );
}
