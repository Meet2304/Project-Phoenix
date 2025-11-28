import Link from 'next/link';
import { Github, Linkedin, ArrowLeft } from 'lucide-react';

// X (Twitter) Logo Component
const XLogo = ({ className }: { className?: string }) => (
    <svg
        viewBox="0 0 24 24"
        className={className}
        fill="currentColor"
        aria-hidden="true"
    >
        <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
    </svg>
);

// const academicGuide = {
//     name: 'Dr. Academic Guide',
//     role: 'Academic Guide & Mentor',
//     avatar: '/images/team/DrMeera.jpg',
//     github: '#',
//     linkedin: '#',
//     twitter: '#',
// };

const members = [
    {
        name: 'Dr. Meera Khanna',
        role: 'Guide & Mentor',
        avatar: '/images/team/DrMeera_1.jpg',
        github: 'https://github.com/Meet2304',
        linkedin: 'https://www.linkedin.com/in/dr-meera-thapar-khanna-892696163/',
        twitter: 'https://twitter.com/meetbhatt',
    },    
    {
        name: 'Meet Bhatt',
        role: 'Project Lead',
        avatar: '/images/team/Meet_Profile_Beach.png',
        github: 'https://github.com/Meet2304',
        linkedin: 'https://linkedin.com/in/meetbhatt',
        twitter: 'https://x.com/Meet2304',
    },
    {
        name: 'Maitri Patel',
        role: 'ML Engineer',
        avatar: '/images/team/Maitri.jpg',
        github: 'https://github.com/maitri0204',
        linkedin: 'https://www.linkedin.com/in/maitri-patel-b42249296/',
        twitter: '#',
    },
    // {
    //     name: 'Devanshi Dudhatra',
    //     role: 'ML Engineer',
    //     avatar: '/images/team/Devanshi.jpeg',
    //     github: 'https://github.com/devanshidudhatra',
    //     linkedin: 'https://www.linkedin.com/in/devanshi-dudhatra-408116253/',
    //     twitter: 'https://x.com/Devanshi0109',
    // },
    // {
    //     name: 'Heet Dobariya',
    //     role: 'Data Scientist',
    //     avatar: '/images/team/Heet.jpeg',
    //     github: 'https://github.com/HeetDobariya07',
    //     linkedin: 'https://www.linkedin.com/in/heet-dobariya-30758a28a/',
    //     twitter: 'https://x.com/HeetDobariya63',
    // },
];

export default function TeamSection() {
    return (
        <section className="flex w-full flex-col items-center justify-center min-h-screen py-16 px-6 sm:px-12 md:px-20 lg:px-32 pb-32 sm:pb-36 md:pb-40">
            <div className="mx-auto max-w-6xl w-full">
                {/* Back Button */}
                <Link href="/" className="inline-flex items-center gap-2 text-white hover:text-white/80 mb-8 md:mb-12 transition-colors group">
                    <ArrowLeft className="w-4 h-4 md:w-5 md:h-5 transition-transform group-hover:-translate-x-1" />
                    <span className="text-sm md:text-base" style={{ fontFamily: "var(--font-poppins)" }}>Back to Home</span>
                </Link>

                <div className="flex flex-col items-center justify-center gap-8 text-center mb-16 px-2">
                    <h1
                        className="font-bold leading-tight text-white drop-shadow-lg"
                        style={{
                            fontFamily: "var(--font-michroma)",
                            fontSize: "clamp(1.75rem, 7vw, 6rem)",
                        }}
                    >
                        OUR DREAM TEAM
                    </h1>
                    <p className="text-white/80 text-base sm:text-lg md:text-xl leading-relaxed max-w-3xl" style={{ fontFamily: "var(--font-playfair)" }}>
                        A dedicated team of researchers and developers working together to revolutionize 
                        cervical cancer cell classification using advanced AI and explainable machine learning techniques.
                    </p>
                </div>

                {/* Team Members */}
                <div className="mt-12 md:mt-16 pb-8">
                    <div className="grid gap-x-8 gap-y-12 sm:gap-y-16 md:grid-cols-2 lg:grid-cols-3 lg:gap-x-8 place-items-center">
                        {members.map((member, index) => (
                            <div key={index} className="group overflow-hidden mb-6 max-w-xs w-full">
                                <img
                                    className="aspect-[3/4] w-full rounded-md object-cover object-top grayscale transition-all duration-500 hover:grayscale-0 group-hover:scale-[0.98] group-hover:rounded-xl"
                                    src={member.avatar}
                                    alt={member.name}
                                    width="826"
                                    height="1239"
                                    loading="lazy"
                                />
                                <div className="px-2 pt-2 sm:pb-0 sm:pt-4">
                                    <div className="flex justify-between">
                                        <h3 className="text-white text-base font-medium transition-all duration-500 group-hover:tracking-wider">
                                            {member.name}
                                        </h3>
                                        <span className="text-white/50 text-xs">_0{index + 1}</span>
                                    </div>
                                    <div className="mt-1 flex items-center justify-between">
                                        <span className="text-white/60 inline-block translate-y-6 text-sm opacity-0 transition duration-300 group-hover:translate-y-0 group-hover:opacity-100">
                                            {member.role}
                                        </span>
                                        <div className="flex gap-3 translate-y-8 opacity-0 transition-all duration-500 group-hover:translate-y-0 group-hover:opacity-100">
                                            <Link
                                                href={member.github}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="text-white/70 hover:text-white transition-colors"
                                                aria-label="GitHub"
                                            >
                                                <Github className="h-4 w-4" />
                                            </Link>
                                            <Link
                                                href={member.linkedin}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="text-white/70 hover:text-white transition-colors"
                                                aria-label="LinkedIn"
                                            >
                                                <Linkedin className="h-4 w-4" />
                                            </Link>
                                            <Link
                                                href={member.twitter}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="text-white/70 hover:text-white transition-colors"
                                                aria-label="X (Twitter)"
                                            >
                                                <XLogo className="h-4 w-4" />
                                            </Link>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </section>
    );
}