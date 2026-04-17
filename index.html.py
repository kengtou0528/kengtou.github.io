<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CBL Terengganu Logistics Explorer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <!-- Chosen Palette: Warm Neutrals (Stone/Sand) with subtle Forest/Amber accents -->
    <!-- Application Structure Plan: The SPA employs a sidebar-navigated, thematic dashboard structure. This design was chosen because expedition logistics involve multiple interconnected but distinct domains (Shelter, Clothing, Nutrition, Safety). A non-linear dashboard allows the user to jump between these functional areas seamlessly, mimicking how a team cross-references packing lists. Interactive components like dynamic packing diagrams, filterable tables, and role-based charts transform static report text into actionable planning tools. -->
    <!-- Visualization & Content Choices: 
         1. Tent/Mat Layout -> Goal: Inform/Organize -> HTML/CSS Grid Visualizer -> Toggle head-to-toe and mat widths -> Demonstrates spatial constraints of the 180cm tent and standard (51cm) vs wide (60cm) mats without external SVG.
         2. Mat Comparison -> Goal: Compare -> JS Data Cards -> Click to switch -> Summarizes pros/cons of air vs foam vs self-inflating mats based on Part 2 of the report.
         3. Nutrition Quantities -> Goal: Inform -> Chart.js Bar Chart & Filterable Table -> Shows aggregate vs daily breakdown.
         4. Team Roles -> Goal: Relationships -> Chart.js Donut -> Click to filter gear -> Visualizes weight distribution and assigns specific gear to P1/P2/P3.
         All visualizations utilize standard HTML/CSS or Chart.js/Canvas, confirming NO SVG or Mermaid JS is used, supporting the interactive explorer structure.
    -->
    <!-- CONFIRMATION: NO SVG graphics used. NO Mermaid JS used. -->

    <style>
        body {
            font-family: 'Inter', sans-serif;
            background-color: #fafaf9; /* stone-50 */
            color: #292524; /* stone-800 */
        }

        /* Mandatory Chart Container Styling */
        .chart-container {
            position: relative;
            width: 100%;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            height: 300px;
            max-height: 400px;
        }

        @media (min-width: 768px) {
            .chart-container {
                height: 350px;
            }
        }

        /* Custom Scrollbar */
        .hide-scroll::-webkit-scrollbar {
            width: 6px;
        }
        .hide-scroll::-webkit-scrollbar-track {
            background: transparent;
        }
        .hide-scroll::-webkit-scrollbar-thumb {
            background-color: #d6d3d1;
            border-radius: 10px;
        }

        /* Tent Visualizer Styles */
        .tent-floor {
            background-color: #e7e5e4;
            border: 4px solid #78716c;
            border-radius: 8px;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 2px;
            overflow: hidden;
            transition: all 0.3s ease;
        }

        .mat {
            height: 95%;
            background-color: #3b82f6;
            border: 2px solid #1d4ed8;
            border-radius: 6px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            align-items: center;
            padding: 8px 0;
            color: white;
            font-size: 0.75rem;
            font-weight: bold;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            opacity: 0.9;
        }

        .mat.reversed {
            flex-direction: column-reverse;
            background-color: #f59e0b; /* amber-500 */
            border-color: #b45309;
        }

        .mat.foam {
            background-color: #10b981; /* emerald-500 */
            border-color: #047857;
            background-image: repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(0,0,0,0.1) 10px, rgba(0,0,0,0.1) 20px);
        }

        .pillow-zone {
            width: 80%;
            height: 20px;
            background-color: rgba(255, 255, 255, 0.4);
            border-radius: 10px;
        }

        /* Active Nav States */
        .nav-active {
            background-color: #292524; /* stone-800 */
            border-left-color: #f59e0b; /* amber-500 */
        }
    </style>
</head>
<body class="flex flex-col md:flex-row min-h-screen">

    <!-- Navigation Sidebar -->
    <nav class="w-full md:w-72 bg-stone-900 text-stone-100 md:fixed md:h-screen flex flex-col shadow-2xl z-50 transition-all">
        <div class="p-6 border-b border-stone-700">
            <h1 class="text-2xl font-bold tracking-tight text-white mb-1">CBL Terengganu</h1>
            <p class="text-sm text-stone-400 font-medium tracking-wide uppercase">Expedition Planner</p>
        </div>
        <div class="flex-1 overflow-y-auto hide-scroll p-4 space-y-2 flex flex-row md:flex-col gap-2 md:gap-0">
            <button onclick="nav('mission')" id="btn-mission" class="nav-btn nav-active flex-shrink-0 w-auto md:w-full text-left px-5 py-3.5 rounded-lg border-l-4 border-amber-500 hover:bg-stone-800 transition-colors duration-200 flex items-center gap-3 font-medium">
                <span class="text-xl">🗺️</span> Mission & Time
            </button>
            <button onclick="nav('shelter')" id="btn-shelter" class="nav-btn flex-shrink-0 w-auto md:w-full text-left px-5 py-3.5 rounded-lg border-l-4 border-transparent hover:bg-stone-800 transition-colors duration-200 flex items-center gap-3 font-medium">
                <span class="text-xl">⛺</span> Shelter System
            </button>
            <button onclick="nav('clothing')" id="btn-clothing" class="nav-btn flex-shrink-0 w-auto md:w-full text-left px-5 py-3.5 rounded-lg border-l-4 border-transparent hover:bg-stone-800 transition-colors duration-200 flex items-center gap-3 font-medium">
                <span class="text-xl">🎒</span> Pack & Clothing
            </button>
            <button onclick="nav('nutrition')" id="btn-nutrition" class="nav-btn flex-shrink-0 w-auto md:w-full text-left px-5 py-3.5 rounded-lg border-l-4 border-transparent hover:bg-stone-800 transition-colors duration-200 flex items-center gap-3 font-medium">
                <span class="text-xl">💧</span> Fuel & Water
            </button>
            <button onclick="nav('safety')" id="btn-safety" class="nav-btn flex-shrink-0 w-auto md:w-full text-left px-5 py-3.5 rounded-lg border-l-4 border-transparent hover:bg-stone-800 transition-colors duration-200 flex items-center gap-3 font-medium">
                <span class="text-xl">🛡️</span> Team & Safety
            </button>
        </div>
    </nav>

    <!-- Main Content Area -->
    <main class="flex-1 md:ml-72 p-4 md:p-8 lg:p-12 pb-24">

        <!-- SECTION: MISSION OVERVIEW -->
        <section id="mission" class="content-section block animate-[fadeIn_0.5s_ease-out]">
            <div class="max-w-5xl mx-auto">
                <div class="mb-10">
                    <h2 class="text-4xl font-bold text-stone-900 mb-4 tracking-tight">Challenge Overview</h2>
                    <p class="text-lg text-stone-600 leading-relaxed max-w-3xl border-l-4 border-amber-500 pl-5 bg-white p-5 rounded-r-xl shadow-sm">
                        This section outlines the core objective of the CBL hiking challenge. The goal is to design and execute a comprehensive logistical strategy utilizing a shared 3-person gear system in the challenging tropical environment of Terengganu. Review the timeline below to understand the operational flow of the 3D2N expedition.
                    </p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-10">
                    <div class="bg-white p-8 rounded-2xl shadow-sm border border-stone-200 hover:shadow-md transition-shadow">
                        <div class="text-3xl mb-3">🎯</div>
                        <h3 class="font-bold text-xl mb-2 text-stone-800">Essential Question</h3>
                        <p class="text-stone-600">How can a team of three maintain safety, comfort, and efficiency during a multi-day hike using limited, shared resources?</p>
                    </div>
                    <div class="bg-white p-8 rounded-2xl shadow-sm border border-stone-200 hover:shadow-md transition-shadow">
                        <div class="text-3xl mb-3">🌴</div>
                        <h3 class="font-bold text-xl mb-2 text-stone-800">Environmental Challenge</h3>
                        <p class="text-stone-600">Endure high humidity, heavy rainfall risks, and heat in Terengganu while optimizing weight distribution and moisture management.</p>
                    </div>
                </div>

                <div class="bg-white p-8 rounded-2xl shadow-sm border border-stone-200">
                    <h3 class="text-2xl font-bold text-stone-800 mb-6">Expedition Timeline</h3>
                    <div class="flex flex-wrap gap-3 mb-8">
                        <button onclick="showTimeline('pre')" id="time-pre" class="px-5 py-2.5 rounded-full bg-amber-500 text-white font-semibold shadow-sm transition-all hover:bg-amber-600">Pre-Trip</button>
                        <button onclick="showTimeline('d1')" id="time-d1" class="px-5 py-2.5 rounded-full bg-stone-100 text-stone-600 font-semibold border border-stone-200 hover:bg-stone-200 transition-all">Day 1</button>
                        <button onclick="showTimeline('d2')" id="time-d2" class="px-5 py-2.5 rounded-full bg-stone-100 text-stone-600 font-semibold border border-stone-200 hover:bg-stone-200 transition-all">Day 2</button>
                        <button onclick="showTimeline('d3')" id="time-d3" class="px-5 py-2.5 rounded-full bg-stone-100 text-stone-600 font-semibold border border-stone-200 hover:bg-stone-200 transition-all">Day 3</button>
                    </div>
                    <div id="timeline-content" class="bg-stone-50 p-6 rounded-xl border border-stone-200 min-h-[160px] transition-opacity duration-300">
                        <h4 class="font-bold text-xl text-stone-800 mb-3 flex items-center gap-2"><span>⏱️</span> Preparation & Logistics</h4>
                        <ul class="list-none text-stone-600 space-y-3">
                            <li class="flex items-start gap-3"><span class="text-emerald-500 mt-1">✓</span> Test-fit mats inside Camel Crown tent.</li>
                            <li class="flex items-start gap-3"><span class="text-emerald-500 mt-1">✓</span> Repackage food; check stove for leaks.</li>
                            <li class="flex items-start gap-3"><span class="text-emerald-500 mt-1">✓</span> Download AllTrails/Gaia maps for offline use.</li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>

        <!-- SECTION: SHELTER SYSTEM -->
        <section id="shelter" class="content-section hidden animate-[fadeIn_0.5s_ease-out]">
            <div class="max-w-5xl mx-auto space-y-10">
                <div>
                    <h2 class="text-4xl font-bold text-stone-900 mb-4 tracking-tight">The "Big Tree" Sleeping System</h2>
                    <p class="text-lg text-stone-600 leading-relaxed max-w-3xl border-l-4 border-amber-500 pl-5 bg-white p-5 rounded-r-xl shadow-sm">
                        This section explores the spatial constraints of the 3-person shelter. It visualizes the strict 180cm floor width limitation, the vital role of the tent's flysheet, and provides an interactive breakdown of sleeping mat technologies. Use the visualizer to understand why specific gear sizing is mandatory.
                    </p>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-start">
                    <!-- Tent Rules -->
                    <div class="bg-white p-8 rounded-2xl shadow-sm border border-stone-200 h-full">
                        <h3 class="text-2xl font-bold text-stone-800 mb-6 flex items-center gap-2"><span>🛡️</span> Tent Anatomy</h3>
                        <div class="space-y-6">
                            <div class="p-5 bg-blue-50 rounded-xl border border-blue-100">
                                <h4 class="font-bold text-blue-900 mb-2 text-lg">The Flysheet Rule</h4>
                                <p class="text-stone-700 leading-relaxed">The flysheet is the waterproof outer layer. In "Serious Mode", it manages condensation from 3 breathing humans. It <strong>MUST be pitched taut</strong>. If it touches the inner mesh, water will seep through via capillary action, soaking the interior.</p>
                            </div>
                            <div class="p-5 bg-stone-50 rounded-xl border border-stone-200">
                                <h4 class="font-bold text-stone-800 mb-2 text-lg">Dimensions & Constraint</h4>
                                <p class="text-stone-600 leading-relaxed">The Camel Crown 3P tent measures <strong>220cm L x 180cm W</strong>. With 3 people, side sleepers will be against the mesh walls, making a taut flysheet absolutely critical for survival.</p>
                            </div>
                        </div>
                    </div>

                    <!-- Interactive Tent Simulator -->
                    <div class="bg-white p-8 rounded-2xl shadow-sm border border-stone-200 h-full flex flex-col items-center">
                        <h3 class="text-2xl font-bold text-stone-800 mb-2">180cm Layout Simulator</h3>
                        <p class="text-sm text-stone-500 mb-6 text-center">Interact with the controls to optimize the floor plan.</p>
                        
                        <div id="tent-visual" class="tent-floor w-full max-w-[300px] aspect-square mb-6 shadow-inner relative">
                            <div class="absolute -top-3 bg-stone-700 text-white text-[10px] px-2 py-0.5 rounded-full z-10 font-bold tracking-wider">180cm WIDTH</div>
                            <!-- Mats generated via JS -->
                            <div class="mat" style="width: 33.33%;"> <div class="pillow-zone"></div> P1 </div>
                            <div class="mat" id="sim-mat-2" style="width: 33.33%;"> <div class="pillow-zone"></div> P2 </div>
                            <div class="mat" style="width: 33.33%;"> <div class="pillow-zone"></div> P3 </div>
                        </div>

                        <div class="w-full space-y-3">
                            <div class="flex justify-between items-center bg-stone-50 p-3 rounded-lg border border-stone-200">
                                <span class="font-medium text-stone-700 text-sm">Mat Width</span>
                                <div class="flex gap-2">
                                    <button onclick="setMatWidth(60)" class="px-3 py-1 bg-stone-800 text-white text-xs rounded hover:bg-stone-700 transition">60cm (Tight)</button>
                                    <button onclick="setMatWidth(51)" class="px-3 py-1 bg-emerald-600 text-white text-xs rounded hover:bg-emerald-700 transition">51cm (Reg)</button>
                                </div>
                            </div>
                            <div class="flex justify-between items-center bg-stone-50 p-3 rounded-lg border border-stone-200">
                                <span class="font-medium text-stone-700 text-sm">Orientation</span>
                                <button onclick="toggleHeadToToe()" class="px-4 py-1 bg-amber-500 text-white text-xs font-bold rounded hover:bg-amber-600 transition shadow-sm flex items-center gap-2">
                                    <span>⇅</span> Head-to-Toe
                                </button>
                            </div>
                        </div>
                        <p id="sim-feedback" class="text-sm font-semibold text-amber-600 mt-4 text-center">3x60cm mats exactly fill 180cm. Shoulders will overlap.</p>
                    </div>
                </div>

                <!-- Mat Analysis (Part 2 Data) -->
                <div class="bg-white p-8 rounded-2xl shadow-sm border border-stone-200">
                    <div class="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-stone-200 pb-4 mb-6">
                        <div>
                            <h3 class="text-2xl font-bold text-stone-800 mb-1">Sleeping Mat Analysis</h3>
                            <p class="text-stone-500 text-sm">Target R-Value for tropical/general: 2.0 - 3.5</p>
                        </div>
                        <div class="flex gap-2 mt-4 md:mt-0 bg-stone-100 p-1 rounded-lg">
                            <button onclick="showMatType('air')" id="btn-mat-air" class="px-4 py-2 rounded-md bg-white shadow-sm text-stone-800 text-sm font-bold transition-all">Air Pad</button>
                            <button onclick="showMatType('foam')" id="btn-mat-foam" class="px-4 py-2 rounded-md text-stone-500 hover:text-stone-800 text-sm font-bold transition-all">Foam</button>
                            <button onclick="showMatType('self')" id="btn-mat-self" class="px-4 py-2 rounded-md text-stone-500 hover:text-stone-800 text-sm font-bold transition-all">Self-Inflate</button>
                        </div>
                    </div>

                    <div id="mat-info-panel" class="grid grid-cols-1 md:grid-cols-3 gap-6 transition-opacity duration-300">
                        <!-- Populated by JS -->
                    </div>
                </div>
            </div>
        </section>

        <!-- SECTION: CLOTHING & PACKING -->
        <section id="clothing" class="content-section hidden animate-[fadeIn_0.5s_ease-out]">
            <div class="max-w-5xl mx-auto space-y-8">
                <div>
                    <h2 class="text-4xl font-bold text-stone-900 mb-4 tracking-tight">Clothing & Pack Architecture</h2>
                    <p class="text-lg text-stone-600 leading-relaxed max-w-3xl border-l-4 border-amber-500 pl-5 bg-white p-5 rounded-r-xl shadow-sm">
                        This section breaks down moisture management and weight distribution. In Terengganu, cotton is strictly avoided. Review the packing lists and interact with the pack diagram below to understand the "Triple Barrier" waterproofing strategy and center of gravity management.
                    </p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <!-- Packing Lists -->
                    <div class="bg-white p-8 rounded-2xl shadow-sm border border-stone-200">
                        <h3 class="text-2xl font-bold text-stone-800 mb-6 border-b border-stone-200 pb-2">Clothing Quantities (3D2N)</h3>
                        <div class="space-y-6">
                            <div class="relative pl-6 border-l-2 border-emerald-500">
                                <span class="absolute -left-3 top-0 text-xl bg-white">🏃</span>
                                <h4 class="font-bold text-stone-800 text-lg mb-2">The "Active" Set</h4>
                                <ul class="text-stone-600 space-y-2">
                                    <li class="flex justify-between border-b border-stone-100 pb-1"><span>Hiking Shirt</span> <b>x2 (Rotate)</b></li>
                                    <li class="flex justify-between border-b border-stone-100 pb-1"><span>Pants/Shorts</span> <b>x1</b></li>
                                    <li class="flex justify-between border-b border-stone-100 pb-1"><span>Underwear</span> <b>x3</b></li>
                                    <li class="flex justify-between border-b border-stone-100 pb-1"><span>Socks (Anti-blister)</span> <b>x3 pairs</b></li>
                                </ul>
                            </div>
                            <div class="relative pl-6 border-l-2 border-amber-500">
                                <span class="absolute -left-3 top-0 text-xl bg-white">🌙</span>
                                <h4 class="font-bold text-stone-800 text-lg mb-2">The "Sacred" Sleep Set</h4>
                                <p class="text-xs font-bold text-amber-600 mb-2 uppercase tracking-wide">Must remain in dry bag</p>
                                <ul class="text-stone-600 space-y-2">
                                    <li class="flex justify-between border-b border-stone-100 pb-1"><span>Camp Shirt & Shorts</span> <b>x1</b></li>
                                    <li class="flex justify-between border-b border-stone-100 pb-1"><span>Sleeping Socks</span> <b>x1 pair</b></li>
                                    <li class="flex justify-between border-b border-stone-100 pb-1"><span>Mid Layer (Fleece)</span> <b>x1</b></li>
                                </ul>
                            </div>
                        </div>
                    </div>

                    <!-- Triple Barrier Pack Visualizer -->
                    <div class="bg-white p-8 rounded-2xl shadow-sm border border-stone-200">
                        <h3 class="text-2xl font-bold text-stone-800 mb-2">Backpack Architecture</h3>
                        <p class="text-sm text-stone-500 mb-6">Hover over layers to reveal packing logic.</p>
                        
                        <div class="relative w-full max-w-[320px] mx-auto h-[350px] bg-stone-100 rounded-t-[3rem] rounded-b-xl p-4 flex flex-col gap-2 border-4 border-stone-300 shadow-inner group">
                            <!-- Pack Cover (Barrier 1) -->
                            <div class="absolute inset-0 border-[3px] border-dashed border-sky-400 rounded-t-[3rem] rounded-b-xl opacity-60 m-1 pointer-events-none"></div>
                            <div class="absolute top-2 right-4 text-[10px] font-bold text-sky-600 uppercase tracking-wider bg-white/80 px-1 rounded">Barrier 1: Cover</div>
                            
                            <!-- Liner (Barrier 2) -->
                            <div class="absolute inset-4 border-2 border-emerald-500 rounded-t-[2.5rem] rounded-b-lg opacity-40 bg-emerald-50/50 z-0 pointer-events-none"></div>
                            <div class="absolute top-6 left-6 text-[10px] font-bold text-emerald-700 uppercase tracking-wider bg-white/80 px-1 rounded z-10">Barrier 2: Liner Bag</div>

                            <!-- Pack Contents -->
                            <div class="relative z-20 flex-[1] mt-10 bg-white border border-stone-300 rounded-lg flex items-center justify-center cursor-help hover:scale-[1.02] hover:shadow-md hover:border-rose-300 transition-all group/item" title="Top Layer: Rain jacket, First Aid, trail snacks, and Day's lunch.">
                                <span class="font-bold text-stone-700 group-hover/item:text-rose-600 transition-colors">Top: Quick Access</span>
                            </div>
                            
                            <div class="relative z-20 flex-[2] bg-white border border-stone-300 rounded-lg flex items-center justify-center cursor-help hover:scale-[1.02] hover:shadow-md hover:border-stone-500 transition-all group/item" title="Middle Layer: Heaviest items. Water, Cook Pot, Gas, Canned Food. Pack against the spine to prevent pulling backward.">
                                <span class="font-bold text-stone-700 group-hover/item:text-stone-900 transition-colors">Middle: Heavy Core</span>
                            </div>
                            
                            <!-- Dry Bag (Barrier 3) -->
                            <div class="relative z-20 flex-[1.5] bg-amber-50 border-2 border-amber-400 rounded-lg flex flex-col items-center justify-center cursor-help hover:scale-[1.02] hover:shadow-md transition-all group/item" title="Bottom Layer: Only needed at camp. Sleeping mat, Sacred Dry Bag. Acts as shock absorption.">
                                <span class="font-bold text-amber-900">Bottom: Camp Gear</span>
                                <span class="text-[10px] font-bold text-amber-700 uppercase mt-1 bg-white/50 px-2 rounded">Barrier 3: Dry Bags</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- SECTION: NUTRITION & HYDRATION -->
        <section id="nutrition" class="content-section hidden animate-[fadeIn_0.5s_ease-out]">
            <div class="max-w-5xl mx-auto space-y-8">
                <div>
                    <h2 class="text-4xl font-bold text-stone-900 mb-4 tracking-tight">Water & Nutrition Strategy</h2>
                    <p class="text-lg text-stone-600 leading-relaxed max-w-3xl border-l-4 border-amber-500 pl-5 bg-white p-5 rounded-r-xl shadow-sm">
                        This section quantifies the fuel required to maintain the 2,500-3,000 daily calorie goal. It presents exact logistical quantities needed per person. Utilize the interactive chart to grasp total volume, and filter the ration table to organize the shared cooking plan.
                    </p>
                </div>

                <!-- Strategy Metrics -->
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
                    <div class="bg-white p-6 rounded-2xl shadow-sm border border-stone-200 flex flex-col items-center text-center">
                        <div class="w-12 h-12 bg-sky-100 text-sky-600 rounded-full flex items-center justify-center text-2xl mb-3">💧</div>
                        <h4 class="font-bold text-stone-800 text-lg">2L Baseline</h4>
                        <p class="text-sm text-stone-500 mt-1">Minimum safety buffer per person. Refuel via river boil + Sawyer filter.</p>
                    </div>
                    <div class="bg-white p-6 rounded-2xl shadow-sm border border-stone-200 flex flex-col items-center text-center">
                        <div class="w-12 h-12 bg-rose-100 text-rose-600 rounded-full flex items-center justify-center text-2xl mb-3">🔥</div>
                        <h4 class="font-bold text-stone-800 text-lg">Shared Cooking</h4>
                        <p class="text-sm text-stone-500 mt-1">1 Canister Stove + 230g Gas + 1.5L Pot. Boil water for 3 servings at once.</p>
                    </div>
                    <div class="bg-white p-6 rounded-2xl shadow-sm border border-stone-200 flex flex-col items-center text-center">
                        <div class="w-12 h-12 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center text-2xl mb-3">⚡</div>
                        <h4 class="font-bold text-stone-800 text-lg">Calorie Target</h4>
                        <p class="text-sm text-stone-500 mt-1">Target ~3,000 cal/day. Avoid heavy box packaging; use Ziplocs.</p>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <!-- Chart -->
                    <div class="bg-white p-8 rounded-2xl shadow-sm border border-stone-200">
                        <h3 class="text-xl font-bold text-stone-800 mb-6">Total Unit Provisions (3D2N)</h3>
                        <div class="chart-container">
                            <canvas id="nutritionChart"></canvas>
                        </div>
                    </div>

                    <!-- Filterable Table -->
                    <div class="bg-white p-8 rounded-2xl shadow-sm border border-stone-200 flex flex-col">
                        <div class="flex justify-between items-center mb-6">
                            <h3 class="text-xl font-bold text-stone-800">Ration Checklist</h3>
                            <select id="meal-filter" class="bg-stone-50 border border-stone-300 text-stone-800 text-sm rounded-lg px-4 py-2 outline-none focus:ring-2 focus:ring-amber-500 transition-shadow font-medium cursor-pointer">
                                <option value="all">All Meals</option>
                                <option value="Breakfast">Breakfast</option>
                                <option value="Lunch">Lunch</option>
                                <option value="Dinner">Dinner</option>
                                <option value="Snacks">Snacks</option>
                            </select>
                        </div>
                        <div class="overflow-x-auto flex-1 border border-stone-200 rounded-xl">
                            <table class="w-full text-left border-collapse">
                                <thead class="bg-stone-50 border-b border-stone-200">
                                    <tr class="text-stone-600 text-xs uppercase tracking-wider">
                                        <th class="p-4 font-bold">Meal</th>
                                        <th class="p-4 font-bold">Item</th>
                                        <th class="p-4 font-bold">Total (3D2N)</th>
                                    </tr>
                                </thead>
                                <tbody id="meal-table-body" class="text-sm divide-y divide-stone-100">
                                    <!-- JS populated -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- SECTION: SAFETY & ROLES -->
        <section id="safety" class="content-section hidden animate-[fadeIn_0.5s_ease-out]">
            <div class="max-w-5xl mx-auto space-y-8">
                <div>
                    <h2 class="text-4xl font-bold text-stone-900 mb-4 tracking-tight">Safety & Team Roles</h2>
                    <p class="text-lg text-stone-600 leading-relaxed max-w-3xl border-l-4 border-amber-500 pl-5 bg-white p-5 rounded-r-xl shadow-sm">
                        This section outlines the distribution of responsibility. Survival is a team effort. By strictly assigning roles and compartmentalizing shared weight, the team ensures nobody is overloaded. Click the chart to filter the gear assignments.
                    </p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-8 items-stretch mb-8">
                    <!-- Donut Chart -->
                    <div class="bg-white p-8 rounded-2xl shadow-sm border border-stone-200 flex flex-col">
                        <h3 class="text-xl font-bold text-stone-800 mb-2">Weight Distribution</h3>
                        <p class="text-sm text-stone-500 mb-6">Click a segment to view specific role responsibilities.</p>
                        <div class="chart-container flex-1">
                            <canvas id="rolesChart"></canvas>
                        </div>
                    </div>
                    
                    <!-- Dynamic Role Card -->
                    <div class="bg-stone-800 text-white p-8 rounded-2xl shadow-lg border border-stone-900 flex flex-col justify-center transition-all duration-300 relative overflow-hidden" id="role-card-bg">
                        <!-- Decorative background element -->
                        <div class="absolute -right-10 -top-10 opacity-10 text-9xl" id="role-icon">👥</div>
                        
                        <div class="relative z-10">
                            <div class="inline-block px-3 py-1 bg-stone-700 rounded-full text-xs font-bold tracking-wider uppercase mb-4 text-stone-300" id="role-tag">Team Operations</div>
                            <h4 id="role-title" class="font-bold text-3xl mb-3">Select a Role</h4>
                            <p id="role-desc" class="text-stone-400 mb-6 text-lg">Review shared responsibility distribution.</p>
                            
                            <div class="bg-stone-900/50 p-5 rounded-xl border border-stone-700 backdrop-blur-sm">
                                <h5 class="text-sm font-bold text-stone-400 uppercase tracking-widest mb-3 border-b border-stone-700 pb-2">Assigned Gear</h5>
                                <ul id="role-gear" class="list-none space-y-3 font-medium">
                                    <li class="flex gap-3 items-center"><span class="text-amber-500">→</span> Click chart to filter gear list.</li>
                                </ul>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Universal Gear -->
                <div class="bg-white p-8 rounded-2xl shadow-sm border border-stone-200">
                    <h3 class="text-xl font-bold text-stone-800 mb-6 border-b border-stone-200 pb-2 flex items-center gap-2"><span>🎒</span> Universal Technical Gear</h3>
                    <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-5">
                        <div class="p-5 border border-stone-100 rounded-xl bg-stone-50 hover:bg-stone-100 transition-colors">
                            <div class="font-bold text-stone-800 text-lg mb-1">Emergency Whistle</div>
                            <div class="text-sm text-stone-500">x3. Keep attached to backpack shoulder strap.</div>
                        </div>
                        <div class="p-5 border border-stone-100 rounded-xl bg-stone-50 hover:bg-stone-100 transition-colors">
                            <div class="font-bold text-stone-800 text-lg mb-1">Offline Maps</div>
                            <div class="text-sm text-stone-500">3 phones. Download AllTrails/Gaia for offline use.</div>
                        </div>
                        <div class="p-5 border border-stone-100 rounded-xl bg-stone-50 hover:bg-stone-100 transition-colors">
                            <div class="font-bold text-stone-800 text-lg mb-1">LED Headlamps</div>
                            <div class="text-sm text-stone-500">x3. Essential for night-time camp tasks.</div>
                        </div>
                        <div class="p-5 border border-stone-100 rounded-xl bg-stone-50 hover:bg-stone-100 transition-colors">
                            <div class="font-bold text-stone-800 text-lg mb-1">Powerbank</div>
                            <div class="text-sm text-stone-500">20,000mAh. 1-2 per group for nav/lights.</div>
                        </div>
                        <div class="p-5 border border-stone-100 rounded-xl bg-stone-50 hover:bg-stone-100 transition-colors">
                            <div class="font-bold text-stone-800 text-lg mb-1">Repair Kit</div>
                            <div class="text-sm text-stone-500">Duct tape, Tenacious Tape, spare buckles.</div>
                        </div>
                        <div class="p-5 border border-stone-100 rounded-xl bg-stone-50 hover:bg-stone-100 transition-colors">
                            <div class="font-bold text-stone-800 text-lg mb-1">Waterproof Lighter</div>
                            <div class="text-sm text-stone-500">x2. Kept in different team members' bags.</div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <!-- Interactive Logic -->
    <script>
        // --- Data Sources (From Report) ---
        const timelineData = {
            'pre': { title: 'Preparation & Logistics', tasks: ['Test-fit 3 mats inside Camel Crown tent.', 'Repackage food; check stove for leaks.', 'Download AllTrails/Gaia for offline use.'] },
            'd1': { title: 'Day 1: Basecamp Entry', tasks: ['Hike Trailhead to Basecamp.', 'Pitch taut flysheet.', 'Heavy Dinner.'] },
            'd2': { title: 'Day 2: Summit Push', tasks: ['Summit exploration.', 'Check for leeches and blisters every 2 hours.', 'Maintain 2L hydration buffer.'] },
            'd3': { title: 'Day 3: Descent', tasks: ['Descent to trailhead.', 'Gear drying process.', 'Team debrief.'] }
        };

        const matComparisonData = {
            'air': { name: 'Inflatable Air Pads', tag: 'Recommended', color: 'text-emerald-700', bg: 'bg-emerald-100', width: 'Regular (51cm)', rval: '2.0 - 3.5', pro: 'Packs to water bottle size, very thick (3-4").', con: 'Can be noisy, higher puncture risk.', ex: 'NEMO Tensor, S2S Ether Light' },
            'foam': { name: 'Closed-Cell Foam', tag: 'Budget', color: 'text-stone-700', bg: 'bg-stone-200', width: 'Standard (51cm)', rval: '~2.0', pro: 'Cheap, indestructible, works as a seat.', con: 'Very bulky, only ~2cm thick.', ex: 'NEMO Switchback, Z-Lite' },
            'self': { name: 'Self-Inflating', tag: 'Quiet', color: 'text-amber-700', bg: 'bg-amber-100', width: 'Varies', rval: '2.5+', pro: 'Mix of foam/air, less bouncy/noisy.', con: 'Heavier and bulkier than pure air.', ex: 'Therm-a-Rest ProLite' }
        };

        const mealData = [
            { type: 'Breakfast', item: 'Instant Oatmeal', qty: '2 pkts / day', total: '6 Packets (~240g)' },
            { type: 'Breakfast', item: 'Milo / Coffee Sachet', qty: '1 sachet / day', total: '3 Sachets' },
            { type: 'Breakfast', item: 'Dried Fruit / Nuts', qty: '1 handful / day', total: '3 Servings' },
            { type: 'Lunch', item: 'Tortilla Wraps', qty: '2 wraps / day', total: '6 Wraps' },
            { type: 'Lunch', item: 'Peanut Butter & Jam', qty: '2-3 tbsp / day', total: '1 Small Jar (Shared)' },
            { type: 'Dinner', item: 'Instant Noodles', qty: '1-2 pkts / day', total: '4-5 Packets' },
            { type: 'Dinner', item: 'Canned Protein', qty: '1 can / day', total: '2 Cans' },
            { type: 'Snacks', item: 'Energy / Cereal Bars', qty: '2 bars / day', total: '6 Bars' },
            { type: 'Snacks', item: 'Trail Mix / Chocolate', qty: '100g / day', total: '300g Total' },
            { type: 'Snacks', item: 'Electrolyte Powder', qty: '1 sachet / day', total: '3 Sachets' }
        ];

        const roleData = {
            0: { tag: 'Person 1', title: 'Navigator', desc: 'Responsible for leading the route and managing the primary shelter structure.', icon: '🗺️', color: 'from-sky-900 to-stone-900', gear: ['Tent Body', 'Tent Poles', 'Offline Maps'] },
            1: { tag: 'Person 2', title: 'Safety & Medic', desc: 'Responsible for health monitoring, weather protection, and emergency response.', icon: '⚕️', color: 'from-emerald-900 to-stone-900', gear: ['Tent Flysheet', 'Tent Stakes', 'Group First Aid Kit (Leukotape, NSAIDs)'] },
            2: { tag: 'Person 3', title: 'Quartermaster', desc: 'Responsible for managing the shared food system, fuel, and clean water processing.', icon: '🔥', color: 'from-amber-900 to-stone-900', gear: ['Cooking System (Stove/Pot)', 'Gas Canister (230g)', 'Shared Food (PB Jar)', 'Water Filter (Sawyer Squeeze)'] },
            'all': { tag: 'Team Operations', title: 'Select a Role', desc: 'Review shared responsibility distribution.', icon: '👥', color: 'from-stone-800 to-stone-900', gear: ['Click chart to filter gear list.'] }
        };

        // --- State Variables ---
        let chartsInit = false;
        let isHeadToToe = false;
        let currentMatWidth = 60; // default 60cm

        // --- Navigation Logic ---
        function nav(sectionId) {
            // Hide all
            document.querySelectorAll('.content-section').forEach(s => s.classList.add('hidden'));
            // Show target
            document.getElementById(sectionId).classList.remove('hidden');
            
            // Update nav buttons
            document.querySelectorAll('.nav-btn').forEach(b => {
                b.classList.remove('nav-active', 'border-amber-500');
                b.classList.add('border-transparent');
            });
            const activeBtn = document.getElementById('btn-' + sectionId);
            activeBtn.classList.add('nav-active', 'border-amber-500');
            activeBtn.classList.remove('border-transparent');

            window.scrollTo({ top: 0, behavior: 'smooth' });

            // Initialize charts on demand
            if (!chartsInit && (sectionId === 'nutrition' || sectionId === 'safety')) {
                initCharts();
                chartsInit = true;
            }
        }

        // --- Mission Timeline Logic ---
        function showTimeline(day) {
            ['pre', 'd1', 'd2', 'd3'].forEach(d => {
                const btn = document.getElementById('time-' + d);
                btn.className = 'px-5 py-2.5 rounded-full bg-stone-100 text-stone-600 font-semibold border border-stone-200 hover:bg-stone-200 transition-all';
            });
            const activeBtn = document.getElementById('time-' + day);
            activeBtn.className = 'px-5 py-2.5 rounded-full bg-amber-500 text-white font-semibold shadow-sm transition-all hover:bg-amber-600';

            const content = document.getElementById('timeline-content');
            content.style.opacity = 0;
            
            setTimeout(() => {
                const iconMap = { 'pre': '⏱️', 'd1': '🚶', 'd2': '⛰️', 'd3': '📉' };
                content.innerHTML = `
                    <h4 class="font-bold text-xl text-stone-800 mb-3 flex items-center gap-2"><span>${iconMap[day]}</span> ${timelineData[day].title}</h4>
                    <ul class="list-none text-stone-600 space-y-3">
                        ${timelineData[day].tasks.map(t => `<li class="flex items-start gap-3"><span class="text-amber-500 mt-1">→</span> ${t}</li>`).join('')}
                    </ul>
                `;
                content.style.opacity = 1;
            }, 150);
        }

        // --- Shelter System Logic ---
        function setMatWidth(width) {
            currentMatWidth = width;
            updateTentVisual();
        }

        function toggleHeadToToe() {
            isHeadToToe = !isHeadToToe;
            updateTentVisual();
        }

        function updateTentVisual() {
            const mats = document.querySelectorAll('.mat');
            const midMat = document.getElementById('sim-mat-2');
            const feedback = document.getElementById('sim-feedback');
            
            // Calculate percentage width based on 180cm total
            // 60cm = 33.33%, 51cm = 28.33%
            const widthPct = (currentMatWidth / 180) * 100;
            
            mats.forEach(mat => {
                mat.style.width = `${widthPct}%`;
            });

            if (isHeadToToe) {
                midMat.classList.add('reversed');
            } else {
                midMat.classList.remove('reversed');
            }

            // Update Feedback
            if (currentMatWidth === 60) {
                feedback.textContent = isHeadToToe ? "3x60cm fills space. Head-to-Toe adds needed shoulder room." : "3x60cm (180cm total). Exact fit. Shoulders will overlap uncomfortably.";
                feedback.className = isHeadToToe ? "text-sm font-semibold text-emerald-600 mt-4 text-center" : "text-sm font-semibold text-amber-600 mt-4 text-center";
            } else {
                feedback.textContent = isHeadToToe ? "3x51cm (153cm total). Plenty of space. Head-to-Toe is luxury." : "3x51cm (153cm total). Recommended setup. Leaves 27cm for gear.";
                feedback.className = "text-sm font-semibold text-emerald-600 mt-4 text-center";
            }
        }

        function showMatType(type) {
            ['air', 'foam', 'self'].forEach(m => {
                const btn = document.getElementById('btn-mat-' + m);
                btn.className = 'px-4 py-2 rounded-md text-stone-500 hover:text-stone-800 text-sm font-bold transition-all';
            });
            document.getElementById('btn-mat-' + type).className = 'px-4 py-2 rounded-md bg-white shadow-sm text-stone-800 text-sm font-bold transition-all';

            const d = matComparisonData[type];
            const panel = document.getElementById('mat-info-panel');
            panel.style.opacity = 0;
            
            setTimeout(() => {
                panel.innerHTML = `
                    <div class="md:col-span-1 bg-stone-50 p-5 rounded-xl border border-stone-200 h-full flex flex-col justify-center">
                        <div class="${d.bg} ${d.color} text-xs font-bold uppercase px-2 py-1 rounded inline-block w-max mb-2">${d.tag}</div>
                        <h4 class="font-bold text-xl text-stone-800 mb-1">${d.name}</h4>
                        <p class="text-sm text-stone-500 italic mb-3">Ex: ${d.ex}</p>
                        <div class="mt-auto">
                            <div class="text-sm border-b border-stone-200 py-1"><span class="font-bold text-stone-700">R-Value:</span> ${d.rval}</div>
                            <div class="text-sm py-1"><span class="font-bold text-stone-700">Width:</span> ${d.width}</div>
                        </div>
                    </div>
                    <div class="md:col-span-2 grid grid-cols-1 sm:grid-cols-2 gap-4">
                        <div class="bg-emerald-50 p-5 rounded-xl border border-emerald-100">
                            <h5 class="font-bold text-emerald-800 mb-2 flex items-center gap-2"><span>⊕</span> Pros</h5>
                            <p class="text-sm text-emerald-700">${d.pro}</p>
                        </div>
                        <div class="bg-rose-50 p-5 rounded-xl border border-rose-100">
                            <h5 class="font-bold text-rose-800 mb-2 flex items-center gap-2"><span>⊖</span> Cons</h5>
                            <p class="text-sm text-rose-700">${d.con}</p>
                        </div>
                    </div>
                `;
                panel.style.opacity = 1;
            }, 150);
        }

        // --- Nutrition Logic ---
        function renderMealTable() {
            const filter = document.getElementById('meal-filter').value;
            const tbody = document.getElementById('meal-table-body');
            tbody.innerHTML = '';
            
            mealData.forEach(m => {
                if(filter === 'all' || m.type === filter) {
                    tbody.innerHTML += `
                        <tr class="hover:bg-amber-50 transition-colors">
                            <td class="p-4 font-semibold text-stone-800 whitespace-nowrap">${m.type}</td>
                            <td class="p-4 text-stone-600">
                                <div>${m.item}</div>
                                <div class="text-xs text-stone-400 mt-0.5">${m.qty}</div>
                            </td>
                            <td class="p-4 font-bold text-emerald-700">${m.total}</td>
                        </tr>
                    `;
                }
            });
        }
        
        // Bind event listener to dropdown
        document.getElementById('meal-filter').addEventListener('change', renderMealTable);


        // --- Initialization & Charts ---
        function initCharts() {
            // Chart 1: Nutrition Quantities (Bar)
            const ctxNut = document.getElementById('nutritionChart').getContext('2d');
            new Chart(ctxNut, {
                type: 'bar',
                data: {
                    labels: ['Oatmeal Pkts', 'Tortilla Wraps', 'Noodle Pkts', 'Energy Bars', 'Powder Sachets'],
                    datasets: [{
                        label: 'Total Units (Per Person)',
                        data: [6, 6, 5, 6, 6],
                        backgroundColor: '#0ea5e9', // sky-500
                        hoverBackgroundColor: '#0284c7', // sky-600
                        borderRadius: 6,
                        barPercentage: 0.6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { 
                            beginAtZero: true, 
                            grid: { color: '#f5f5f4' }, // stone-100
                            ticks: { stepSize: 1, font: { family: 'Inter', size: 12 } },
                            title: { display: true, text: 'Total Units Needed', font: {family: 'Inter'} }
                        },
                        x: { 
                            grid: { display: false }, 
                            ticks: { font: { family: 'Inter', size: 11 } } 
                        }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            backgroundColor: '#292524',
                            titleFont: {family: 'Inter'},
                            bodyFont: {family: 'Inter'},
                            padding: 10,
                            callbacks: {
                                title: function(context) {
                                    // Label wrapping logic (max ~16 chars)
                                    let raw = context[0].label;
                                    let words = raw.split(' ');
                                    let lines = [], current = '';
                                    words.forEach(w => {
                                        if((current + w).length > 16) { lines.push(current); current = w + ' '; }
                                        else { current += w + ' '; }
                                    });
                                    lines.push(current.trim());
                                    return lines;
                                }
                            }
                        }
                    }
                }
            });

            // Chart 2: Roles Distribution (Doughnut)
            const ctxRole = document.getElementById('rolesChart').getContext('2d');
            new Chart(ctxRole, {
                type: 'doughnut',
                data: {
                    labels: ['Person 1: Navigator', 'Person 2: Medic', 'Person 3: Quartermaster'],
                    datasets: [{
                        data: [33.3, 33.3, 33.4],
                        backgroundColor: ['#0ea5e9', '#10b981', '#f59e0b'], // sky, emerald, amber
                        borderWidth: 3,
                        borderColor: '#ffffff',
                        hoverOffset: 10
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    cutout: '70%',
                    plugins: {
                        legend: { 
                            position: 'bottom', 
                            labels: { font: { family: 'Inter', size: 12 }, padding: 20, usePointStyle: true } 
                        },
                        tooltip: {
                            callbacks: { label: (ctx) => ` 1/3 Group Weight` }
                        }
                    },
                    onClick: (evt, elements) => {
                        if (elements.length > 0) {
                            updateRoleCard(elements[0].index);
                        } else {
                            updateRoleCard('all');
                        }
                    }
                }
            });
        }

        function updateRoleCard(index) {
            const data = roleData[index];
            const bg = document.getElementById('role-card-bg');
            
            // Apply gradient based on role
            bg.className = `bg-gradient-to-br ${data.color} text-white p-8 rounded-2xl shadow-lg border border-stone-900 flex flex-col justify-center transition-all duration-500 relative overflow-hidden`;
            
            document.getElementById('role-tag').textContent = data.tag;
            document.getElementById('role-title').textContent = data.title;
            document.getElementById('role-desc').textContent = data.desc;
            document.getElementById('role-icon').textContent = data.icon;
            
            document.getElementById('role-gear').innerHTML = data.gear.map(g => 
                `<li class="flex gap-3 items-center"><span class="text-amber-500">→</span> ${g}</li>`
            ).join('');
        }

        // --- Run on Load ---
        document.addEventListener('DOMContentLoaded', () => {
            showMatType('air');
            renderMealTable();
        });

    </script>
</body>
</html>