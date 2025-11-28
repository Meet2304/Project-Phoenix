"use client";

import { motion, useScroll, useTransform } from "framer-motion";
import React, { useRef } from "react";
import { FeatureShowcase } from "./feature-showcase";
import Link from "next/link";
import { ArrowLeft } from "lucide-react";

const processSteps = [
  {
    position: "right",
    yPosition: "top-[100vh]",
    title: "Data Preprocessing",
    description: "Transform raw microscopy images into analysis-ready data through advanced preprocessing techniques.",
    stats: ["Image Enhancement", "Noise Reduction", "Standardization"],
    steps: [
      {
        id: "preprocessing-1",
        title: "Where did we get the images from?",
        text: `Our pipeline begins with high-quality cytology images sourced from two benchmark datasets — the <a href="https://www.kaggle.com/datasets/prahladmehandiratta/cervical-cancer-largest-dataset-sipakmed" target="_blank" rel="noopener noreferrer">SIPaKMeD dataset</a> and the <a href="https://www.kaggle.com/datasets/yuvrajsinhachowdhury/herlev-dataset/data" target="_blank" rel="noopener noreferrer">Herlev dataset</a>. These collections provide diverse, expertly labeled cervical cell images that form the foundation for reliable preprocessing, model training, and explainable AI development.`
      },
      {
        id: "preprocessing-2",
        title: "How did we improve the images?",
        text: "We cleaned noise using Non-Local Means (NLM), enhanced brightness and contrast using CLAHE, and normalized the colors so the cell images became clearer, sharper, and more consistent for training."
      },
      {
        id: "preprocessing-3",
        title: "What data augmentation techniques did we use?",
        text: "We used rotations, flips, zooming, shifting, and light color variations to make the model learn from many different versions of each cell image."
      }
    ],
    image: {
      src: "/images/About/Image Preprocesing_v0.1.jpg",
      alt: "Data preprocessing pipeline"
    },
    learnMoreLink: "/preprocessing",
    githubLink: "https://github.com/Meet2304/Project-Phoenix/tree/main/Image%20Preprocessing"
  },
  {
    position: "left",
    yPosition: "top-[225vh]",
    title: "Model Fine-Tuning",
    description: "Leverage transfer learning with state-of-the-art ConvNeXt architecture for precise cell classification.",
    stats: ["Transfer Learning", "95%+ Accuracy"],
    steps: [
      {
        id: "training-1",
        title: "Which pre-trained backbones did we choose?",
        text: "We built our models on EfficientNetV2-S and ConvNeXt, two state-of-the-art backbones known for capturing subtle cellular details with exceptional clarity."
      },
      {
        id: "training-2",
        title: "How did we fine-tune the model?",
        text: "We fine-tuned the higher layers on our cleaned and augmented SIPaKMeD + Herlev dataset, allowing the models to learn nucleus boundaries, cytoplasm textures, and cell-type specific visual cues."
      },
      {
        id: "training-3",
        title: "How did we validate and test the model?",
        text: "We validated using stratified splits across both datasets and tested on held-out samples to ensure the models generalize across staining variations, microscope settings, and cell subtypes."
      }
    ],
    image: {
      src: "/images/About/Model Finetuning_v0.1.jpg",
      alt: "Model fine-tuning process"
    },
    learnMoreLink: "/model-training",
    githubLink: "https://github.com/Meet2304/Project-Phoenix/tree/main/Fine%20Tuning"
  },
  {
    position: "right",
    yPosition: "top-[350vh]",
    title: "Explainability",
    description: "Build trust through transparent AI decision-making with advanced visualization techniques.",
    stats: ["Grad-CAM", "Attention Maps", "Feature Attribution"],
    steps: [
      {
        id: "explain-1",
        title: "How does our model reveal the features it uses to classify cervical cells?",
        text: "We combine Concept-Guided Attention Maps (CGAM), SHAP, and nuclear segmentation masks to highlight the exact nuclear borders, cytoplasmic regions, and texture cues driving each prediction."
      },
      {
        id: "explain-2",
        title: "How do we ensure the explanations align with real cytology concepts?",
        text: "We anchor the model’s explanations to biologically meaningful nuclear features—like nuclear enlargement, hyperchromasia, and boundary irregularity—using segmentation masks as precise structural guides."
      },
      {
        id: "explain-3",
        title: "How do we compare explanations across different models?",
        text: "We generate side-by-side explanation panels using attention maps, SHAP overlays, and segmentation masks to see how EfficientNetV2-S and ConvNeXt differ in highlighting clinically relevant regions."
      }
    ],
    image: {
      src: "/images/About/Model Explanability_v0.6.jpg",
      alt: "Explainability visualization"
    },
    learnMoreLink: "/explainability",
    githubLink: "https://github.com/Meet2304/Project-Phoenix/tree/main/Explainability%20Workflows"
  },
  {
    position: "left",
    yPosition: "top-[475vh]",
    title: "Performance Evaluation",
    description: "Comprehensive assessment using clinical-grade metrics and real-world validation.",
    stats: ["Multi-Class Metrics", "Confusion Matrix", "ROC Analysis"],
    steps: [
      {
        id: "eval-1",
        title: "How do we measure how well the model identifies different cervical cell types?",
        text: "We evaluate performance using accuracy, F1-score, and class-wise precision/recall, ensuring the model reliably distinguishes normal, abnormal, and borderline cell classes across both datasets."
      },
      {
        id: "eval-2",
        title: "How do we assess whether the model generalizes across staining styles and microscope variations?",
        text: "We test on held-out samples from SIPaKMeD and Herlev, checking consistency across different color tones, imaging conditions, and morphological variations."
      },
      {
        id: "eval-3",
        title: "How do we verify that high performance aligns with meaningful explanations?",
        text: "We pair metric evaluation with explanation-quality checks—comparing SHAP, attention maps, and nuclear segmentation masks to confirm the model focuses on real cytological structures, not noise."
      }
    ],
    image: {
      src: "/images/About/Performance Eval_v0.1.jpg",
      alt: "Performance evaluation metrics"
    },
    learnMoreLink: "/evaluation",
    githubLink: "https://github.com/Meet2304/Project-Phoenix/tree/main/Explainability%20Workflows"
  }
];

const Skiper19 = () => {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({
    target: ref,
  });

  return (
    <section
      ref={ref}
      className="relative mx-auto flex h-auto md:h-[625vh] w-screen flex-col items-center overflow-visible bg-transparent text-white"
    >
      {/* Back Button */}
      <div className="w-full px-6 sm:px-8 md:px-12 lg:px-16 pt-12 md:pt-20 z-20">
        <Link href="/" className="inline-flex items-center gap-2 text-white hover:text-white/80 transition-colors group mb-6 md:mb-8">
          <ArrowLeft className="w-4 h-4 md:w-5 md:h-5 transition-transform group-hover:-translate-x-1" />
          <span className="text-sm md:text-base" style={{ fontFamily: "var(--font-poppins)" }}>Back to Home</span>
        </Link>
      </div>

      {/* Desktop SVG Line */}
      <LinePath
        className="hidden md:block absolute left-1/2 -translate-x-1/2 top-0 z-0 w-[90vw] max-w-[1200px]"
        scrollYProgress={scrollYProgress}
      />
      
      {/* Mobile SVG Line */}
      <MobileLinePath
        className="md:hidden absolute left-0 top-0 z-0 w-[60px]"
        scrollYProgress={scrollYProgress}
      />
      <div className="mt-4 md:mt-20 relative flex w-full max-w-[95vw] mx-auto flex-col items-center justify-center gap-3 md:gap-5 text-center mb-12 md:mb-32 z-10 px-6 md:px-8">
        <h1 className="relative z-10 text-5xl sm:text-6xl md:text-8xl font-medium tracking-[0.15em] sm:tracking-[0.2em] md:tracking-[0.4em] lg:text-9xl leading-tight" style={{ fontFamily: "var(--font-michroma)" }}>
          ABOUT
        </h1>
      </div>

      {/* Introduction paragraph */}
      <div className="relative md:absolute md:top-[50vh] w-full z-10 px-8 md:px-16 lg:px-24 mb-12 md:mb-0 mt-12 md:mt-0">
        <div className="max-w-3xl mx-auto text-center space-y-4 md:space-y-6">
          <p className="text-base sm:text-lg md:text-xl lg:text-2xl text-white/90 leading-relaxed font-normal" style={{ fontFamily: "var(--font-playfair)" }}>
            Project Phoenix reimagines cervical cancer cell classification with a fully transparent AI pipeline. The journey begins with high-quality data preprocessing, ensuring clean and reliable cytology inputs. We then fine-tune advanced deep learning models to recognize subtle cellular patterns with precision. Every prediction is made interpretable through explainability techniques that reveal the features driving the model's decisions. Finally, rigorous performance evaluation demonstrates not only how accurately the system works — but why its judgments can be trusted.
          </p>
          {/* <p className="text-lg text-white/70 leading-relaxed" style={{ fontFamily: "var(--font-poppins)" }}>
            Through meticulous data preprocessing, transfer learning with ConvNeXt models, and transparent explainability features, 
            we empower healthcare professionals with reliable AI-driven insights for improved patient outcomes in cervical cancer screening.
          </p> */}
        </div>
      </div>

      {/* Feature showcases at each curve */}
      {/* Mobile wrapper with spacing */}
      <div className="relative w-full space-y-12 md:hidden">
      {processSteps.map((step, index) => (
        <div key={index} className="relative w-full z-10 px-8">
          <div className="max-w-5xl mx-auto">
            <FeatureShowcase
              eyebrow={`Step ${index + 1}`}
              title={step.title}
              description={step.description}
              stats={step.stats}
              steps={step.steps}
              image={step.image}
              learnMoreLink={step.learnMoreLink}
              githubLink={step.githubLink}
              panelMinHeight={600}
              className="bg-transparent"
              flip={step.position === "left"}
            />
          </div>
        </div>
      ))}
      </div>
      
      {/* Desktop absolute positioned cards */}
      {processSteps.map((step, index) => (
        <div
          key={index}
          className={`hidden md:block absolute ${step.yPosition} w-full z-10 px-12 lg:px-20 xl:px-32`}
        >
          <div className={`max-w-5xl mx-auto ${step.position === "left" ? "mr-auto" : "ml-auto"}`}>
            <FeatureShowcase
              eyebrow={`Step ${index + 1}`}
              title={step.title}
              description={step.description}
              stats={step.stats}
              steps={step.steps}
              image={step.image}
              learnMoreLink={step.learnMoreLink}
              githubLink={step.githubLink}
              panelMinHeight={600}
              className="bg-transparent"
              flip={step.position === "left"}
            />
          </div>
        </div>
      ))}
    </section>
  );
};

export { Skiper19 };

const LinePath = ({
  className,
  scrollYProgress,
}: {
  className: string;
  scrollYProgress: any;
}) => {
  const pathLength = useTransform(scrollYProgress, [0, 1], [0, 1]);

  return (
    <svg
      width="100%"
      height="625vh"
      viewBox="0 0 1000 5500"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      preserveAspectRatio="xMidYMin meet"
      style={{ pointerEvents: 'none' }}
    >
      <motion.path
        d="M500 0 C550 50, 600 100, 700 200 C850 350, 900 500, 800 700 C700 900, 500 1000, 300 1200 C100 1400, 150 1600, 350 1800 C550 2000, 750 2100, 850 2300 C950 2500, 900 2700, 700 2900 C500 3100, 300 3300, 400 3600 C500 3900, 650 4200, 750 4500 C850 4800, 750 5000, 650 5200 C550 5400, 500 5500, 500 5500"
        stroke="rgba(255, 255, 255, 0.9)"
        strokeWidth="30"
        fill="none"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeDasharray="1"
        strokeDashoffset="1"
        style={{
          pathLength,
        }}
      />
    </svg>
  );
};

const MobileLinePath = ({
  className,
  scrollYProgress,
}: {
  className: string;
  scrollYProgress: any;
}) => {
  const pathLength = useTransform(scrollYProgress, [0, 1], [0, 1]);

  return (
    <svg
      width="100%"
      height="100%"
      viewBox="0 0 100 3000"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      preserveAspectRatio="none"
      style={{ pointerEvents: 'none', minHeight: '100%' }}
    >
      <motion.path
        d="M30 0 C45 100, 20 200, 35 300 C50 400, 25 500, 40 600 C55 700, 20 800, 30 900 C45 1000, 25 1100, 40 1200 C55 1300, 20 1400, 30 1500 C45 1600, 25 1700, 40 1800 C50 1900, 25 2000, 35 2100 C50 2200, 20 2300, 35 2400 C50 2500, 25 2600, 35 2700 C45 2800, 25 2900, 30 3000"
        stroke="rgba(255, 255, 255, 0.9)"
        strokeWidth="20"
        fill="none"
        strokeLinecap="round"
        strokeLinejoin="round"
        strokeDasharray="1"
        strokeDashoffset="1"
        style={{
          pathLength,
        }}
      />
    </svg>
  );
};

