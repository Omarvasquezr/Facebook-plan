/* Contenuti tradotti localmente: nessun invio di dati a servizi di traduzione. */
(() => {
  'use strict';
  const languages = ['it', 'es', 'en'];
  const content = [
  [
    "Disponibile · Santa Marinella (RM)",
    "Disponible · Santa Marinella (RM)",
    "Available · Santa Marinella (RM)"
  ],
  [
    "Chiama",
    "Llamar",
    "Call"
  ],
  [
    "Email",
    "Email",
    "Email"
  ],
  [
    "Faccio funzionare le cose:",
    "Hago que las cosas funcionen:",
    "I make things work:"
  ],
  [
    "squadre, conti, clienti.",
    "equipos, cuentas, clientes.",
    "teams, numbers, clients."
  ],
  [
    "Un'attività non cresce per caso.",
    "Un negocio no crece por casualidad.",
    "A business doesn’t grow by chance."
  ],
  [
    "Cresce quando qualcuno tiene i conti, il gruppo e il cliente nella stessa mano. L'ho fatto in un reparto d'albergo, in un'agenzia con clienti in sei paesi e in un'impresa mia.",
    "Crece cuando alguien conecta las cuentas, el equipo y el cliente. Lo he hecho en el departamento de un hotel, en una agencia con clientes en seis países y en mi propio negocio.",
    "It grows when someone brings the numbers, the team and the client together. I’ve done that in a hotel department, at an agency with clients in six countries and in my own business."
  ],
  [
    "In Italia",
    "En Italia",
    "In Italy"
  ],
  [
    "Sono ripartito dal lavaggio e dalla sala: a chi fa questo mestiere da una vita non si arriva a spiegare niente,",
    "En Italia empecé de nuevo, lavando platos y atendiendo mesas. Ante quienes llevan toda una vida en este oficio,",
    "In Italy, I started again, washing dishes and waiting tables. When you work alongside people who have spent a lifetime in the trade,"
  ],
  [
    "prima si impara.",
    "lo primero es aprender.",
    "you learn first."
  ],
  [
    "anni, dal 2011",
    "años, desde 2011",
    "years, since 2011"
  ],
  [
    "Fino a tre allestimenti in una sola giornata, in stagioni da oltre duecento eventi.",
    "Hasta tres montajes en un día, en temporadas de más de doscientos eventos.",
    "Up to three setups in a day, in seasons with over two hundred events."
  ],
  [
    "vendite di un reparto all'Hotel Pullman (Accor)",
    "ventas de un departamento del Hotel Pullman (Accor)",
    "department sales at Hotel Pullman (Accor)"
  ],
  [
    "Riorganizzando processi, costi, servizi e formando la squadra commerciale.",
    "Reorganizando procesos, costes y servicios, y formando al equipo comercial.",
    "By reorganising processes, costs and services, and training the sales team."
  ],
  [
    "Non con pubblicità.",
    "Sin recurrir a publicidad.",
    "Without advertising."
  ],
  [
    "paesi serviti",
    "países atendidos",
    "countries served"
  ],
  [
    "dall'agenzia",
    "por la agencia",
    "by the agency"
  ],
  [
    "lingue",
    "idiomas",
    "languages"
  ],
  [
    "Spagnolo",
    "Español",
    "Spanish"
  ],
  [
    "madrelingua",
    "nativo",
    "native"
  ],
  [
    "Inglese",
    "Inglés",
    "English"
  ],
  [
    "Italiano",
    "Italiano",
    "Italian"
  ],
  [
    "intermedio-avanzato",
    "intermedio-avanzado",
    "intermediate–advanced"
  ],
  [
    "Capacità",
    "Capacidades",
    "Skills"
  ],
  [
    "Guidare una squadra",
    "Liderar un equipo",
    "Leading a team"
  ],
  [
    "Tecnici, fornitori e team multidisciplinari in eventi corporate e alberghieri; ritmo nelle ore di punta.",
    "Técnicos, proveedores y equipos multidisciplinares en eventos corporativos y hoteleros; coordinación en las horas de mayor actividad.",
    "Technicians, suppliers and multidisciplinary teams at corporate and hotel events; keeping things moving at peak times."
  ],
  [
    "Analizzare e ottimizzare",
    "Analizar y optimizar",
    "Analysing and improving"
  ],
  [
    "Leggere un'attività, trovare dove si perde il margine e rimetterla in ordine: processi, costi, fornitori, budget e reportistica alla proprietà.",
    "Entender un negocio, detectar dónde se pierde margen y poner orden: procesos, costes, proveedores, presupuestos e informes a la propiedad.",
    "Understanding a business, finding where margins are lost and getting things in order: processes, costs, suppliers, budgets and reporting to owners."
  ],
  [
    "Scala",
    "Trabajar a escala",
    "Working at scale"
  ],
  [
    "Centinaia di eventi, dai matrimoni alle serate in discoteca, dagli eventi corporate in albergo alle attivazioni di marca che si vedono da tutta una città.",
    "Cientos de eventos: desde bodas y noches de discoteca hasta encuentros corporativos en hoteles y activaciones de marca visibles en toda una ciudad.",
    "Hundreds of events, from weddings and club nights to corporate events at hotels and brand activations visible across a city."
  ],
  [
    "Digitale e IA",
    "Digital e IA",
    "Digital and AI"
  ],
  [
    "Campagne Meta, Google e TikTok Ads; automazione delle prenotazioni via telefono e WhatsApp; gestione clienti; siti web.",
    "Campañas en Meta, Google y TikTok Ads; automatización de reservas por teléfono y WhatsApp; gestión de clientes y sitios web.",
    "Meta, Google and TikTok Ads campaigns; booking automation by phone and WhatsApp; client management and websites."
  ],
  [
    "Percorso",
    "Trayectoria",
    "My journey"
  ],
  [
    "Imparare il mestiere",
    "Aprender el oficio",
    "Learning the trade"
  ],
  [
    "Tecnico audiovisivo a Caracas. Mi sono dedicato a imparare tutto sul campo: audio, illuminazione, visuali, allestimento. Un'ingegneria del suono fatta per pura pratica.",
    "Técnico audiovisual en Caracas. Me dediqué a aprender sobre el terreno: audio, iluminación, visuales y montaje. Aprendizaje del sonido a través de la práctica.",
    "An audiovisual technician in Caracas. I focused on learning on the job: audio, lighting, visuals and setup. Learning sound through hands-on experience."
  ],
  [
    "Da tecnico a produttore",
    "De técnico a productor",
    "From technician to producer"
  ],
  [
    "Coordinatore di allestimenti molto giovane, in contatto con i grandi nomi della produzione a Caracas. Poi il Cile, ripartendo dal basso fino alle principali società di eventi corporate del paese.",
    "Coordiné montajes desde muy joven, trabajando con referentes de la producción en Caracas. Después llegó Chile: empezar de nuevo y avanzar hasta trabajar con importantes empresas de eventos corporativos del país.",
    "I became a setup coordinator at a young age, working with leading production professionals in Caracas. Then came Chile: starting again and working my way up to major corporate events companies."
  ],
  [
    "Dentro l'albergo",
    "Dentro del hotel",
    "Inside the hotel"
  ],
  [
    "RLA-Latam gestisce il reparto audiovisivo dentro gli hotel. Sono entrato come tecnico e dopo tre mesi mi hanno promosso a responsabile del reparto all'Hotel Pullman Vitacura (Accor): vendite, costi, personale e rapporto diretto con la direzione.",
    "RLA-Latam gestiona departamentos audiovisuales dentro de hoteles. Entré como técnico y, tras tres meses, me ascendieron a responsable del departamento del Hotel Pullman Vitacura (Accor): ventas, costes, personal y relación directa con la dirección.",
    "RLA-Latam runs audiovisual departments within hotels. I joined as a technician and, after three months, was promoted to department manager at Hotel Pullman Vitacura (Accor): sales, costs, staff and direct contact with hotel management."
  ],
  [
    "Impresa mia",
    "Mi propio negocio",
    "My own business"
  ],
  [
    "Quando la pandemia ha fermato gli eventi non mi sono fermato io: ho fondato un e-commerce con piano di import-export e mi sono formato nel marketing digitale. Cambiare mestiere senza perdere il passo.",
    "Cuando la pandemia detuvo los eventos, busqué otro camino: fundé un comercio electrónico con un plan de importación y exportación y me formé en marketing digital. Cambiar de actividad sin perder el ritmo.",
    "When the pandemic stopped events, I found another path: I founded an e-commerce business with an import-export plan and trained in digital marketing. Changing direction without losing momentum."
  ],
  [
    "Mi chiamavano loro",
    "Me buscaban a mí",
    "They called me"
  ],
  [
    "Diverse società di produzione mi cercavano come coordinatore di allestimenti e attivazioni, e per farsi consigliare nella pianificazione con il cliente. Reputazione e modo di lavorare.",
    "Varias productoras me buscaban para coordinar montajes y activaciones, y para asesorarlas en la planificación con el cliente. Una relación basada en mi reputación y mi forma de trabajar.",
    "Production companies approached me to coordinate setups and activations, and to advise on planning with clients. It came down to reputation and how I work."
  ],
  [
    "Il salto",
    "El salto",
    "The next step"
  ],
  [
    "Dalla produzione alla direzione: marketing, relazioni pubbliche, consulenza commerciale e creazione di esperienze, lanci ed eventi, questa volta da capo. Responsabile dei clienti di un'agenzia con mercati in sei paesi, fino alla chiusura ordinata delle attività.",
    "De la producción a la dirección: marketing, relaciones públicas, asesoría comercial y creación de experiencias, lanzamientos y eventos, esta vez al frente. Responsable de los clientes de una agencia con mercados en seis países, hasta el cierre ordenado de sus actividades.",
    "From production to leadership: marketing, public relations, sales consulting and creating experiences, launches and events, this time in charge. Managing clients at an agency operating in six countries, through to its orderly closure."
  ],
  [
    "Italia, dal basso",
    "Italia, empezar de nuevo",
    "Italy, starting again"
  ],
  [
    "Lavapiatti e cameriere sul litorale romano, e l'italiano da imparare. Nel 2026 cameriere, pittura e carpenteria nella ristrutturazione di un chiosco sul mare, e poi barman.",
    "Lavaplatos y camarero en la costa romana, mientras aprendía italiano. En 2026, servicio de mesas, pintura y carpintería durante la reforma de un quiosco junto al mar, y después trabajo de barman.",
    "Washing dishes and waiting tables on the Roman coast, while learning Italian. In 2026, table service, painting and carpentry during the renovation of a seaside kiosk, followed by bartending."
  ],
  [
    "Esperienza",
    "Experiencia",
    "Experience"
  ],
  [
    "dal 2011",
    "desde 2011",
    "since 2011"
  ],
  [
    "Cameriere, allestimento e barman",
    "Camarero, montaje y barman",
    "Waiter, setup and bartender"
  ],
  [
    "Pittura, carpenteria e allestimento durante la ristrutturazione del locale, poi servizio in sala e al banco.",
    "Pintura, carpintería y montaje durante la reforma del local; después, servicio de mesas y barra.",
    "Painting, carpentry and setup during the venue’s renovation, followed by table and bar service."
  ],
  [
    "Lavapiatti e cameriere",
    "Lavaplatos y camarero",
    "Kitchen porter and waiter"
  ],
  [
    "Direttore clienti e team leader",
    "Director de cuentas y líder de equipo",
    "Client director and team leader"
  ],
  [
    "Aguacate Comunicaciones (Cile, da remoto)",
    "Aguacate Comunicaciones (Chile, en remoto)",
    "Aguacate Comunicaciones (Chile, remote)"
  ],
  [
    "6 paesi · marchi portati da zero alla redditività",
    "6 países · marcas acompañadas desde cero hasta la rentabilidad",
    "6 countries · brands guided from launch to profitability"
  ],
  [
    "Portfolio di clienti di settori, lingue, paesi e dimensioni di mercato diversi: Panduit, Adagio Teas, FLY Racing, Nutrición en Balance, Astara, Taller Phantom, Ares Consulting, Darkone, FELS Latino e Bark in Style. Direzione e supervisione delle strategie di comunicazione interna ed esterna, marketing e relazioni pubbliche. Coordinamento dei team di lavoro dei diversi clienti e, insieme agli specialisti di ogni area, supervisione dei processi amministrativi e contabili nei paesi in cui operavamo: Cile, Perù, Argentina, Colombia, Spagna e Italia. Marchi accompagnati da zero fino a diventare attività redditizie. Chiusura ordinata dell'agenzia.",
    "Cartera de clientes de distintos sectores, idiomas, países y tamaños de mercado: Panduit, Adagio Teas, FLY Racing, Nutrición en Balance, Astara, Taller Phantom, Ares Consulting, Darkone, FELS Latino y Bark in Style. Dirección y supervisión de estrategias de comunicación interna y externa, marketing y relaciones públicas. Coordinación de los equipos de los distintos clientes y, junto a los especialistas de cada área, supervisión de procesos administrativos y contables en Chile, Perú, Argentina, Colombia, España e Italia. Acompañamiento de marcas desde cero hasta convertirse en negocios rentables. Cierre ordenado de la agencia.",
    "A client portfolio spanning different sectors, languages, countries and market sizes: Panduit, Adagio Teas, FLY Racing, Nutrición en Balance, Astara, Taller Phantom, Ares Consulting, Darkone, FELS Latino and Bark in Style. Leading and overseeing internal and external communications, marketing and public relations strategies. Coordinating client teams and working with specialists to oversee administrative and accounting processes in Chile, Peru, Argentina, Colombia, Spain and Italy. Guiding brands from launch to profitable businesses. Managing the agency’s orderly closure."
  ],
  [
    "Coordinatore di montaggi e attivazioni — freelance",
    "Coordinador de montajes y activaciones — freelance",
    "Setup and activation coordinator — freelance"
  ],
  [
    "MAGIX Producciones · Vibra Producciones · Lafirma Producciones (Santiago del Cile)",
    "MAGIX Producciones · Vibra Producciones · Lafirma Producciones (Santiago de Chile)",
    "MAGIX Producciones · Vibra Producciones · Lafirma Producciones (Santiago, Chile)"
  ],
  [
    "Montaggi di schermi LED e attivazioni di marca. Tra queste, nel team tecnico dell'attivazione con cui il BCI ha annunciato la sponsorizzazione della Nazionale cilena: comunicazione, direzione sul campo e coordinamento del personale e della logistica.",
    "Montaje de pantallas LED y activaciones de marca. Entre ellas, formé parte del equipo técnico de la activación con la que BCI anunció su patrocinio de la selección chilena: comunicación, dirección sobre el terreno y coordinación de personal y logística.",
    "LED screen setups and brand activations. These included working in the technical team for the activation announcing BCI’s sponsorship of Chile’s national football team: communications, on-site direction, and staff and logistics coordination."
  ],
  [
    "Consulente",
    "Consultor",
    "Consultant"
  ],
  [
    "Darkone, Bark in Style e FELS Latino: clienti portati da me in agenzia. Strategia, pianificazione e reportistica.",
    "Darkone, Bark in Style y FELS Latino: clientes que incorporé a la agencia. Estrategia, planificación e informes.",
    "Darkone, Bark in Style and FELS Latino: clients I brought to the agency. Strategy, planning and reporting."
  ],
  [
    "Imprenditore",
    "Emprendedor",
    "Entrepreneur"
  ],
  [
    "Impresa fondata da me · import-export",
    "Empresa fundada por mí · importación y exportación",
    "Business I founded · import-export"
  ],
  [
    "E-commerce di giardinaggio e coltivazione indoor con piano di import-export.",
    "Comercio electrónico de jardinería y cultivo de interior con un plan de importación y exportación.",
    "An e-commerce business for gardening and indoor growing, with an import-export plan."
  ],
  [
    "Community manager",
    "Community manager",
    "Community manager"
  ],
  [
    "Responsabile del dipartimento audiovisivo",
    "Responsable del departamento audiovisual",
    "Audiovisual department manager"
  ],
  [
    "+25% vendite del reparto",
    "+25% en ventas del departamento",
    "+25% in department sales"
  ],
  [
    "Tecnico audiovisivo",
    "Técnico audiovisual",
    "Audiovisual technician"
  ],
  [
    "Senior Event Producer",
    "Productor sénior de eventos",
    "Senior event producer"
  ],
  [
    "Tecnico audiovisivo e produttore",
    "Técnico audiovisual y productor",
    "Audiovisual technician and producer"
  ],
  [
    "Strumenti",
    "Herramientas",
    "Tools"
  ],
  [
    "Consolle audio",
    "Consolas de audio",
    "Audio consoles"
  ],
  [
    "Illuminazione robotizzata",
    "Iluminación robotizada",
    "Moving-head lighting"
  ],
  [
    "Schermi LED",
    "Pantallas LED",
    "LED screens"
  ],
  [
    "Claude e strumenti di IA",
    "Claude y herramientas de IA",
    "Claude and AI tools"
  ],
  [
    "Formazione",
    "Formación",
    "Education"
  ],
  [
    "Titolo universitario venezuelano in Studi Internazionali",
    "Título universitario venezolano en Estudios Internacionales",
    "Venezuelan university degree in International Studies"
  ],
  [
    "Università Santa María, Caracas · Facoltà di Giurisprudenza · 2011–2016 (titolo 2018)",
    "Universidad Santa María, Caracas · Facultad de Derecho · 2011–2016 (título expedido en 2018)",
    "Universidad Santa María, Caracas · Faculty of Law · 2011–2016 (degree issued in 2018)"
  ],
  [
    "Un percorso di cinque anni tra diritto, economia e relazioni internazionali. Mi ha lasciato il modo di lavorare che uso ogni giorno: analizzare una situazione prima di decidere, negoziare, muovermi tra mercati e culture diverse e scrivere in modo che si capisca.",
    "Cinco años de formación en derecho, economía y relaciones internacionales. De allí viene mi forma de trabajar: analizar antes de decidir, negociar, desenvolverme entre mercados y culturas diferentes y escribir con claridad.",
    "Five years studying law, economics and international relations. It shaped how I work today: analysing a situation before deciding, negotiating, navigating different markets and cultures, and writing clearly."
  ],
  [
    "Contatti · Disponibile",
    "Contacto · Disponible",
    "Contact · Available"
  ],
  [
    "Da portare con sé, in PDF.",
    "Para llevar contigo, en PDF.",
    "Take it with you, in PDF."
  ],
  [
    "Formato schermo",
    "PDF horizontal",
    "Landscape PDF"
  ],
  [
    "Italiano · computer",
    "Italiano · ordenador",
    "Italian · desktop"
  ],
  [
    "Formato verticale",
    "PDF vertical",
    "Portrait PDF"
  ],
  [
    "Italiano · telefono",
    "Italiano · teléfono",
    "Italian · mobile"
  ],
  [
    "Come è nata questa pagina",
    "Cómo nació esta página",
    "How this page came to life"
  ],
  [
    "L'ho costruita insieme a Claude, l'intelligenza artificiale di Anthropic, in uno spazio di lavoro controllato. Le regole con cui ha lavorato l'IA, l'identità, le idee e ogni contenuto sono miei; la realizzazione l'abbiamo fatta insieme.",
    "La construí junto a Claude, la inteligencia artificial de Anthropic, en un espacio de trabajo controlado. Las reglas de trabajo de la IA, la identidad, las ideas y el contenido son míos; la desarrollamos juntos.",
    "I built it with Claude, Anthropic’s AI, in a controlled workspace. The rules for the AI, the identity, ideas and content are mine; we developed it together."
  ],
  [
    "Autorizzo il trattamento dei dati personali ai sensi del D.Lgs. 196/2003 e del Regolamento UE 2016/679 (GDPR).",
    "Autorizo el tratamiento de mis datos personales conforme al Decreto Legislativo italiano 196/2003 y al Reglamento UE 2016/679 (RGPD).",
    "I authorise the processing of my personal data under Italian Legislative Decree 196/2003 and EU Regulation 2016/679 (GDPR)."
  ]
];
  const ui = {
  "navigation": [
    "Contatti e preferenze",
    "Contacto y preferencias",
    "Contact and preferences"
  ],
  "chooseLanguage": [
    "Scegli la lingua",
    "Elegir idioma",
    "Choose language"
  ],
  "languageHeading": [
    "Lingua del sito",
    "Idioma de la web",
    "Website language"
  ],
  "darkMode": [
    "Modalità scura",
    "Modo oscuro",
    "Dark mode"
  ],
  "callOmar": [
    "Chiama Omar",
    "Llamar a Omar",
    "Call Omar"
  ],
  "appearance": [
    "Aspetto",
    "Apariencia",
    "Appearance"
  ],
  "lightYourWay": [
    "La luce, come piace a te.",
    "La luz, a tu manera.",
    "A little light, your way."
  ],
  "day": [
    "Giorno",
    "Día",
    "Day"
  ],
  "night": [
    "Notte",
    "Noche",
    "Night"
  ],
  "darkSelected": [
    "Modalità scura attivata.",
    "Modo oscuro activado.",
    "Dark mode on."
  ],
  "lightSelected": [
    "Modalità chiara attivata.",
    "Modo claro activado.",
    "Light mode on."
  ],
  "languageSelected": [
    "Lingua impostata: italiano.",
    "Idioma elegido: español.",
    "Language set to English."
  ],
  "pdfNote": [
    "I PDF attuali sono in italiano.",
    "Los PDF actuales están en italiano.",
    "The current PDFs are in Italian."
  ],
  "description": [
    "Omar Vásquez — eventi, produzione audiovisiva, marketing e gestione. Santa Marinella (RM).",
    "Omar Vásquez — eventos, producción audiovisual, marketing y gestión. Santa Marinella (RM).",
    "Omar Vásquez — events, audiovisual production, marketing and management. Santa Marinella (RM)."
  ],
  "ogDescription": [
    "Faccio funzionare le cose: squadre, conti, clienti.",
    "Hago que las cosas funcionen: equipos, cuentas, clientes.",
    "I make things work: teams, numbers, clients."
  ],
  "shareImageAlt": [
    "Omar Vásquez. Portfolio e CV. Eventi, produzione e marketing, in blu e arancione.",
    "Omar Vásquez. Portfolio y CV. Eventos, producción y marketing, en azul y naranja.",
    "Omar Vásquez. Portfolio and CV. Events, production and marketing, in blue and orange."
  ]
};
  const root = document.documentElement;
  const stored = key => { try { return localStorage.getItem(key); } catch (_) { return null; } };
  const remember = (key, value) => { try { localStorage.setItem(key, value); } catch (_) { /* Preferenze valide comunque nella scheda corrente. */ } };
  const dictionary = new Map(content.map(row => [row[0], row]));
  const nodes = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (node.parentElement.closest('script,style,noscript,[data-ui],[data-language],#preference-status')) continue;
    const key = node.nodeValue.trim();
    if (dictionary.has(key)) nodes.push({ node, key, original: node.nodeValue });
  }
  const status = document.getElementById('preference-status');
  const trigger = document.getElementById('language-toggle');
  const panel = document.getElementById('language-panel');
  const picker = document.querySelector('.language-picker');
  const options = [...panel.querySelectorAll('[data-language]')];
  const systemTheme = matchMedia('(prefers-color-scheme: dark)');
  let language = languages.includes(stored('ov-language')) ? stored('ov-language') : 'it';
  let explicitTheme = ['light','dark'].includes(stored('ov-theme')) ? stored('ov-theme') : null;
  const text = key => ui[key][languages.indexOf(language)];

  function applyLanguage(next, announce = false) {
    language = languages.includes(next) ? next : 'it';
    const index = languages.indexOf(language);
    root.lang = language;
    nodes.forEach(({ node, key, original }) => {
      node.nodeValue = original.replace(key, () => dictionary.get(key)[index]);
    });
    document.querySelectorAll('[data-ui]').forEach(el => { el.textContent = text(el.dataset.ui); });
    document.querySelectorAll('[data-label]').forEach(el => { el.setAttribute('aria-label', text(el.dataset.label)); });
    options.forEach(el => el.setAttribute('aria-pressed', String(el.dataset.language === language)));
    document.querySelector('meta[name="description"]').content = text('description');
    document.querySelector('meta[property="og:description"]').content = text('ogDescription');
    document.querySelector('meta[name="twitter:description"]').content = text('ogDescription');
    document.querySelector('meta[property="og:locale"]').content = { it:'it_IT', es:'es_ES', en:'en_GB' }[language];
    document.querySelector('meta[property="og:image:alt"]').content = text('shareImageAlt');
    document.querySelector('meta[name="twitter:image:alt"]').content = text('shareImageAlt');
    if (announce) status.textContent = text('languageSelected');
  }

  function applyTheme(next, announce = false) {
    const dark = next === 'dark';
    root.dataset.theme = dark ? 'dark' : 'light';
    document.querySelectorAll('[data-theme-toggle]').forEach(button => button.setAttribute('aria-checked', String(dark)));
    document.querySelector('meta[name="theme-color"]').content = dark ? '#080F20' : '#F2F4F7';
    if (announce) status.textContent = text(dark ? 'darkSelected' : 'lightSelected');
  }

  function closeLanguages(returnFocus = false) {
    panel.hidden = true;
    trigger.setAttribute('aria-expanded', 'false');
    if (returnFocus) trigger.focus();
  }
  trigger.addEventListener('click', () => {
    if (!panel.hidden) { closeLanguages(); return; }
    panel.hidden = false;
    trigger.setAttribute('aria-expanded', 'true');
    options.find(el => el.dataset.language === language).focus();
  });
  options.forEach(button => button.addEventListener('click', () => {
    remember('ov-language', button.dataset.language);
    applyLanguage(button.dataset.language, true);
    closeLanguages(true);
  }));
  picker.addEventListener('keydown', event => {
    if (event.key === 'Escape' && !panel.hidden) { event.preventDefault(); closeLanguages(true); }
    if (!panel.hidden && ['ArrowDown','ArrowUp','Home','End'].includes(event.key)) {
      event.preventDefault();
      const current = options.indexOf(document.activeElement);
      const index = event.key === 'Home' ? 0 : event.key === 'End' ? options.length - 1 : (current + (event.key === 'ArrowDown' ? 1 : -1) + options.length) % options.length;
      options[index].focus();
    }
  });
  document.addEventListener('click', event => { if (!picker.contains(event.target)) closeLanguages(); });
  picker.addEventListener('focusout', event => { if (!picker.contains(event.relatedTarget)) closeLanguages(); });
  document.querySelectorAll('[data-theme-toggle]').forEach(button => button.addEventListener('click', () => {
    explicitTheme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    remember('ov-theme', explicitTheme);
    applyTheme(explicitTheme, true);
  }));
  systemTheme.addEventListener('change', event => { if (!explicitTheme) applyTheme(event.matches ? 'dark' : 'light'); });
  addEventListener('storage', event => {
    if (event.key === 'ov-language' || event.key === null) applyLanguage(stored('ov-language'));
    if (event.key === 'ov-theme' || event.key === null) {
      const value = stored('ov-theme');
      explicitTheme = ['light','dark'].includes(value) ? value : null;
      applyTheme(explicitTheme || (systemTheme.matches ? 'dark' : 'light'));
    }
  });
  applyLanguage(language);
  applyTheme(explicitTheme || (systemTheme.matches ? 'dark' : 'light'));
})();
