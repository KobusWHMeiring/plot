<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
<head>
<meta charset="utf-8"/>
<meta content="width=device-width, initial-scale=1.0" name="viewport"/>
<title>Plot | Systems Architecture for Landscaping</title>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&amp;family=Playfair+Display:ital,wght@0,400;0,700;1,400;1,700&amp;display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&amp;display=swap" rel="stylesheet"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,typography,container-queries"></script>
<script>
        tailwind.config = {
            darkMode: "class",
            theme: {
                extend: {
                    colors: {
                        primary: "#1A3A17", // Deeper Forest Green
                        accent: "#D4AF37", // Gold accent for premium feel
                        "background-light": "#F9FBF9", 
                        "background-dark": "#0A0F0B",
                    },
                    fontFamily: {
                        sans: ["Plus Jakarta Sans", "sans-serif"],
                        serif: ["Playfair Display", "serif"],
                    },
                    borderRadius: {
                        DEFAULT: "4px",
                    },
                },
            },
        };
    </script>
<style type="text/tailwindcss">
        :root {
            --primary-color: #1A3A17;
        }
        body {
            font-family: 'Plus Jakarta Sans', sans-serif;
        }
        h1, h2, h3, .font-serif {
            font-family: 'Playfair Display', serif;
        }
        .glass-card {
            background: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(26, 58, 23, 0.1);
        }
        .dark .glass-card {
            background: rgba(15, 23, 16, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
    </style>
</head>
<body class="bg-background-light dark:bg-background-dark text-slate-800 dark:text-slate-100 transition-colors duration-300">
<nav class="sticky top-0 z-50 bg-background-light/95 dark:bg-background-dark/95 backdrop-blur-md border-b border-green-100/50 dark:border-green-900/20">
<div class="max-w-7xl mx-auto px-6 h-24 flex items-center justify-between">
<div class="flex items-center gap-3">
<span class="material-symbols-outlined text-primary dark:text-white text-4xl">hub</span>
<span class="font-serif text-3xl tracking-tight text-primary dark:text-white font-bold italic">Plot.</span>
</div>
<div class="hidden md:flex items-center gap-10">
<a class="text-sm font-semibold tracking-widest uppercase hover:text-primary transition-colors" href="#methodology">Methodology</a>
<a class="text-sm font-semibold tracking-widest uppercase hover:text-primary transition-colors" href="#solution">The OS</a>
<button class="bg-primary text-white px-8 py-3 rounded-none font-bold hover:bg-black transition-all shadow-xl">
                REQUEST AUDIT
            </button>
</div>
</div>
</nav>

<!-- Hero Section -->
<section class="relative overflow-hidden pt-16 pb-24 md:pt-32 md:pb-40">
<div class="max-w-7xl mx-auto px-6 grid lg:grid-cols-2 gap-20 items-center">
<div class="space-y-10">
<div class="inline-flex items-center gap-3 px-4 py-1.5 border-l-2 border-accent bg-primary/5 text-primary dark:text-white font-bold text-xs uppercase tracking-[0.2em]">
                Systems Architecture &amp; Design
            </div>
<h1 class="text-5xl md:text-7xl font-bold text-primary dark:text-white leading-[0.95] text-balance">
                Enterprise efficiency for the <span class="italic font-normal font-serif text-primary/80 dark:text-emerald-400">modern landscape.</span>
</h1>
<p class="text-xl md:text-2xl text-slate-600 dark:text-slate-300 max-w-xl leading-relaxed font-light">
                We don't just build websites. We install an <strong>Operational Operating System</strong> that optimizes your margins, workflows, and client retention.
            </p>
<div class="flex flex-col sm:flex-row gap-6 items-start sm:items-center">
<button class="bg-primary text-white px-10 py-5 rounded-none font-bold text-lg hover:bg-black transition-all shadow-2xl">
                    View The Architecture
                </button>
</div>
</div>

<!-- Visual Metaphor: Process Flow -->
<div class="relative hidden md:block">
<div class="absolute inset-0 bg-primary/5 rounded-full blur-3xl -z-10 transform scale-110"></div>
<div class="grid grid-cols-1 gap-8 relative">
    
    <!-- Floating "Fintech" Badge -->
    <div class="absolute -top-12 right-12 z-20 bg-white dark:bg-slate-800 p-4 shadow-lg border-l-4 border-accent max-w-[200px]">
        <p class="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Background</p>
        <p class="text-sm font-serif italic text-primary dark:text-white">Built by Fintech & LegalTech Product Managers.</p>
    </div>

    <!-- The Plot Card -->
    <div class="relative transform rotate-0 transition-transform duration-500 z-10">
        <div class="bg-white dark:bg-slate-900 p-2 shadow-[0_50px_100px_-20px_rgba(26,58,23,0.3)] border border-primary/10">
            <div class="bg-background-light dark:bg-slate-800 p-8 space-y-6">
                <!-- Header -->
                <div class="flex justify-between items-center border-b border-primary/10 pb-4">
                    <div class="font-serif text-xl italic text-primary dark:text-white">Workflow Automation</div>
                    <span class="material-symbols-outlined text-green-600">sync_alt</span>
                </div>
                <!-- Flow Chart Visualization -->
                <div class="space-y-4">
                    <div class="flex items-center gap-4">
                        <div class="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center text-xs font-bold text-slate-500">1</div>
                        <div class="h-10 flex-1 bg-white border border-slate-200 flex items-center px-4 text-xs font-mono text-slate-500">
                            Ingest: Handwriting OCR
                        </div>
                    </div>
                    <div class="flex items-center gap-4">
                        <div class="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center text-xs font-bold text-slate-500">2</div>
                        <div class="h-10 flex-1 bg-white border border-slate-200 flex items-center px-4 text-xs font-mono text-slate-500">
                            Process: Margin Calc
                        </div>
                    </div>
                    <div class="flex items-center gap-4">
                        <div class="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center text-xs font-bold">3</div>
                        <div class="h-10 flex-1 bg-primary text-white flex items-center px-4 text-xs font-bold tracking-widest uppercase justify-between">
                            Output: Profit & Billing
                            <span class="material-symbols-outlined text-sm">check_circle</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
</div>
</section>

<!-- The Methodology Section (New) -->
<section class="py-24 bg-white dark:bg-slate-950 border-y border-slate-100 dark:border-slate-900" id="methodology">
    <div class="max-w-7xl mx-auto px-6">
        <div class="grid md:grid-cols-2 gap-16 items-center">
            <div>
                <span class="text-accent font-bold tracking-[0.3em] uppercase text-xs mb-6 block">The Philosophy</span>
                <h2 class="text-4xl font-bold text-primary dark:text-white mb-6 font-serif">
                    Run your garden service like a <span class="italic text-slate-500">tech company.</span>
                </h2>
                <p class="text-lg text-slate-600 dark:text-slate-400 leading-relaxed mb-6">
                    In Fintech, a lost decimal point is a crisis. In Landscaping, a lost job card is "business as usual." We disagree.
                </p>
                <p class="text-lg text-slate-600 dark:text-slate-400 leading-relaxed mb-8">
                    We bring <strong>Systems Thinking</strong> to the garden. We identify bottlenecks, automate the grunt work, and give you the data visibility usually reserved for Fortune 500 companies.
                </p>
                <div class="flex gap-4">
                    <div class="px-4 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 rounded text-xs font-bold uppercase tracking-widest text-slate-500">Process First</div>
                    <div class="px-4 py-2 bg-slate-50 dark:bg-slate-900 border border-slate-200 rounded text-xs font-bold uppercase tracking-widest text-slate-500">Data Driven</div>
                </div>
            </div>
            <div class="grid grid-cols-2 gap-4">
                <div class="glass-card p-6">
                    <span class="text-4xl font-serif italic text-accent block mb-2">80%</span>
                    <span class="text-sm font-bold uppercase tracking-widest text-primary dark:text-white">Admin Reduction</span>
                </div>
                <div class="glass-card p-6">
                    <span class="text-4xl font-serif italic text-accent block mb-2">100%</span>
                    <span class="text-sm font-bold uppercase tracking-widest text-primary dark:text-white">Billable Capture</span>
                </div>
                <div class="glass-card p-6 col-span-2">
                    <span class="text-4xl font-serif italic text-accent block mb-2">Zero</span>
                    <span class="text-sm font-bold uppercase tracking-widest text-primary dark:text-white">Hardware Required</span>
                    <p class="text-xs text-slate-400 mt-2">We optimize for the paper-based reality of the field.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- The Transformation Section (Re-framed) -->
<section class="py-24 bg-primary text-white relative overflow-hidden" id="the-deal">
<div class="absolute inset-0 opacity-10 pointer-events-none">
<svg class="h-full w-full" preserveAspectRatio="none" viewBox="0 0 100 100">
<path d="M0 100 L100 0 L100 100 Z" fill="currentColor"></path>
</svg>
</div>
<div class="max-w-7xl mx-auto px-6 relative z-10">
<div class="grid lg:grid-cols-2 gap-20 items-center">
<div>
<span class="text-accent font-bold tracking-[0.3em] uppercase text-xs mb-6 block">The Transformation</span>
<h2 class="text-4xl md:text-6xl font-bold mb-8 leading-tight font-serif">We build the engine.<br><span class="text-emerald-400 italic">You keep the profit.</span></h2>
<p class="text-xl text-emerald-100/70 mb-10 font-light leading-relaxed">
    Plot functions as your outsourced <strong>Product Team</strong>. We analyze your workflows, install the Harvester OS to automate them, and build the client-facing digital infrastructure to support them.
</p>
</div>
<div class="grid grid-cols-1 gap-6">
<div class="glass-card bg-white/5 border-white/10 p-10 hover:bg-white/10 transition-colors">
<div class="flex justify-between items-start mb-4">
    <h3 class="text-2xl font-bold">1. The Core OS</h3>
    <span class="material-symbols-outlined text-accent">memory</span>
</div>
<p class="text-emerald-100/60 leading-relaxed mb-4">Implementation of <strong>Harvester</strong>. AI handwriting recognition, margin analysis, and logistics planning.</p>
<ul class="text-xs font-mono text-accent uppercase tracking-widest space-y-1">
    <li>+ Automate Invoicing</li>
    <li>+ Digitise Archives</li>
</ul>
</div>

<div class="glass-card bg-white/5 border-white/10 p-10 hover:bg-white/10 transition-colors">
<div class="flex justify-between items-start mb-4">
    <h3 class="text-2xl font-bold">2. The Digital Interface</h3>
    <span class="material-symbols-outlined text-accent">web</span>
</div>
<p class="text-emerald-100/60 leading-relaxed mb-4">
    We build a bespoke company website that acts as the secure <strong>Client Portal</strong>. It’s not just a brochure; it’s where your clients interact with your system.
</p>
<ul class="text-xs font-mono text-accent uppercase tracking-widest space-y-1">
    <li>+ Brand Modernization</li>
    <li>+ Secure Client Access</li>
</ul>
</div>
</div>
</div>
</div>
</section>

<!-- Solution Section -->
<section class="py-32 bg-background-light dark:bg-slate-900" id="solution">
<div class="max-w-7xl mx-auto px-6">
<div class="flex flex-col items-center mb-24 text-center">
<span class="text-primary dark:text-emerald-400 font-bold tracking-[.4em] uppercase text-xs mb-6">System Capabilities</span>
<h2 class="text-4xl md:text-6xl font-bold text-slate-900 dark:text-white">Seamless Horticultural Tech</h2>
</div>
<div class="grid lg:grid-cols-3 gap-16">
<div class="group">
<div class="text-6xl font-serif italic text-primary/10 mb-[-2rem] group-hover:text-primary/20 transition-colors">01</div>
<div class="space-y-6 relative z-10">
<h3 class="text-3xl font-bold dark:text-white">AI Handwriting Engine</h3>
<p class="text-primary dark:text-emerald-400 font-bold italic font-serif">"Keep the Paper. Automate the Data."</p>
<p class="text-slate-600 dark:text-slate-400 leading-relaxed">
                        Snap one photo, and our Vision AI reads the handwriting and digitizes it instantly. Zero training time for field staff.
                    </p>
</div>
</div>
<div class="group">
<div class="text-6xl font-serif italic text-primary/10 mb-[-2rem] group-hover:text-primary/20 transition-colors">02</div>
<div class="space-y-6 relative z-10">
<h3 class="text-3xl font-bold dark:text-white">"Magic Link" Portal</h3>
<p class="text-primary dark:text-emerald-400 font-bold italic font-serif">"The Waitrose of Maintenance."</p>
<p class="text-slate-600 dark:text-slate-400 leading-relaxed">
                        Clients receive a branded email with a secure link to visit summaries, feedback loops, and a plant wishlist.
                    </p>
</div>
</div>
<div class="group">
<div class="text-6xl font-serif italic text-primary/10 mb-[-2rem] group-hover:text-primary/20 transition-colors">03</div>
<div class="space-y-6 relative z-10">
<h3 class="text-3xl font-bold dark:text-white">Operational Intelligence</h3>
<p class="text-primary dark:text-emerald-400 font-bold italic font-serif">"Know your Numbers."</p>
<p class="text-slate-600 dark:text-slate-400 leading-relaxed">
                        Automatic shopping lists and profit tracking. See exactly what inputs are used vs. what you are billing.
                    </p>
</div>
</div>
</div>
</div>
</section>

<!-- Call to Action -->
<section class="py-24 px-6">
<div class="max-w-5xl mx-auto bg-primary text-white p-12 md:p-24 relative overflow-hidden shadow-2xl">
<div class="absolute top-0 right-0 w-96 h-96 bg-accent/10 rounded-full -mr-48 -mt-48 blur-3xl"></div>
<div class="relative z-10 text-center space-y-12">
<h2 class="text-4xl md:text-6xl font-bold font-serif italic">Optimize your operations.</h2>
<p class="text-xl text-emerald-100/80 max-w-2xl mx-auto font-light leading-relaxed">
                We are currently accepting three new landscaping partners for this quarter. Let's discuss how we can streamline your business.
            </p>
<button class="bg-white text-primary px-12 py-6 rounded-none font-bold text-xl hover:bg-accent hover:text-white transition-colors shadow-2xl tracking-widest uppercase">
                Request Strategy Call
            </button>
</div>
</div>
</section>

<footer class="py-20 px-6 border-t border-green-100 dark:border-green-900/30 bg-background-light dark:bg-slate-950">
<div class="max-w-7xl mx-auto grid md:grid-cols-4 gap-12">
<div class="col-span-2">
<div class="flex items-center gap-3 mb-8">
<span class="material-symbols-outlined text-primary dark:text-white text-3xl">hub</span>
<span class="font-serif text-2xl font-bold italic text-primary dark:text-white">Plot.</span>
</div>
<p class="text-slate-500 dark:text-slate-400 max-w-xs leading-relaxed">
                Systems Architecture & Process Optimization for the Landscaping Industry.
            </p>
</div>
<div>
<h4 class="font-bold uppercase tracking-widest text-xs mb-6 text-slate-400">Navigation</h4>
<ul class="space-y-4 text-sm font-semibold dark:text-slate-300">
<li><a class="hover:text-primary transition-colors" href="#">Methodology</a></li>
<li><a class="hover:text-primary transition-colors" href="#">Case Studies</a></li>
<li><a class="hover:text-primary transition-colors" href="#">Contact</a></li>
</ul>
</div>
<div>
<h4 class="font-bold uppercase tracking-widest text-xs mb-6 text-slate-400">Legal</h4>
<ul class="space-y-4 text-sm font-semibold dark:text-slate-300">
<li><a class="hover:text-primary transition-colors" href="#">Privacy</a></li>
<li><a class="hover:text-primary transition-colors" href="#">Terms</a></li>
</ul>
</div>
</div>
<div class="max-w-7xl mx-auto mt-20 pt-10 border-t border-slate-100 dark:border-slate-900 flex flex-col md:row justify-between items-center gap-6">
<p class="text-slate-400 text-xs tracking-widest uppercase">
            © 2026 Plot Architecture. All rights reserved.
        </p>
</div>
</footer>
<script>
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.classList.add('dark');
    }
</script>

</body></html>