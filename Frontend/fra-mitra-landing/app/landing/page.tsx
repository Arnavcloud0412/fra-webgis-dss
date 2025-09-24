import Header from "@/components/Header";
import Hero from "@/components/Hero";
import IssuesCarousel from "@/components/IssuesCarousel";
import MapSection from "@/components/MapSection";
import FRAIntro from "@/components/FRAIntro";
import Footer from "@/components/Footer";

export default function LandingPage() {
  return (
    <div className="bg-white min-h-screen">
      <Header />
      <main>
        <Hero />
        <IssuesCarousel />
        <MapSection />
        <FRAIntro />
      </main>
      <Footer />
    </div>
  );
}
