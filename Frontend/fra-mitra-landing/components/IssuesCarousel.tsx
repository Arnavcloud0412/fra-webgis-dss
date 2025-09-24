'use client';

import React from 'react';
import { Swiper, SwiperSlide } from 'swiper/react';
import { Autoplay, Pagination } from 'swiper/modules';
import 'swiper/css';
import 'swiper/css/pagination';
import { FileText, Users, Map, BarChart, ShieldAlert } from 'lucide-react';

const issues = [
  {
    text: "Over 200+ Tribal Communities still fighting for land rights",
    icon: <Users className="h-8 w-8 text-white/80" />,
    bg: "bg-gradient-to-br from-purple-500 to-indigo-600",
  },
  {
    text: "Millions of acres lost due to lack of proper documents",
    icon: <FileText className="h-8 w-8 text-white/80" />,
    bg: "bg-gradient-to-br from-rose-500 to-pink-600",
  },
  {
    text: "Lack of transparency in FRA monitoring",
    icon: <ShieldAlert className="h-8 w-8 text-white/80" />,
    bg: "bg-gradient-to-br from-amber-500 to-orange-600",
  },
  {
    text: "Difficulty accessing welfare schemes",
    icon: <BarChart className="h-8 w-8 text-white/80" />,
    bg: "bg-gradient-to-br from-teal-500 to-cyan-600",
  },
  {
    text: "Fragmented data across states",
    icon: <Map className="h-8 w-8 text-white/80" />,
    bg: "bg-gradient-to-br from-lime-500 to-green-600",
  },
];

const IssuesCarousel = () => {
  return (
    <section className="bg-gray-50 py-16 sm:py-24">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-3xl font-extrabold text-center text-gray-900 mb-12">
          Challenges in FRA Implementation
        </h2>
        <Swiper
          modules={[Autoplay, Pagination]}
          spaceBetween={30}
          slidesPerView={1.2}
          centeredSlides={true}
          autoplay={{
            delay: 3000,
            disableOnInteraction: false,
          }}
          pagination={{ clickable: true }}
          loop={true}
          breakpoints={{
            640: {
              slidesPerView: 2,
              spaceBetween: 20,
            },
            768: {
              slidesPerView: 3,
              spaceBetween: 40,
            },
            1024: {
              slidesPerView: 4,
              spaceBetween: 50,
            },
          }}
          className="!pb-12"
        >
          {issues.map((issue, index) => (
            <SwiperSlide key={index}>
              <div className={`p-6 rounded-xl shadow-lg h-48 flex flex-col justify-between text-white ${issue.bg}`}>
                {issue.icon}
                <p className="font-semibold text-lg">{issue.text}</p>
              </div>
            </SwiperSlide>
          ))}
        </Swiper>
      </div>
    </section>
  );
};

export default IssuesCarousel;
