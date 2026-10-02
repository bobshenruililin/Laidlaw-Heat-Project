// Update the same 10-slide internal briefing from checked aggregate inputs.
// Runtime locations may be overridden without modifying bundled dependencies.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const runtime=process.env.LAIDLAW_NODE_MODULES??'/Users/macbookpro/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules';
// The bundled validator resolves its package through this documented variable.
process.env.RUNTIME_NODE_MODULES=runtime;
const skill=process.env.LAIDLAW_PRESENTATION_SKILL??'/Users/macbookpro/.codex/plugins/cache/openai-primary-runtime/presentations/26.904.11930/skills/presentations';
const python=process.env.LAIDLAW_RUNTIME_PYTHON??'/Users/macbookpro/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';
const {Presentation,PresentationFile}=await import(pathToFileURL(path.join(runtime,'@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const {resolvePresentationFont,applyPresentationChartFont,finalizePresentation}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const font=resolvePresentationFont({fontFamily:'Arial'});
const p=Presentation.create({slideSize:{width:1280,height:720}});
const navy='#183343',teal='#14685F',ink='#283D47',muted='#576971',red='#8C4052';
const build=path.join(root,'.research-build/evidence-briefing');
const finaldir=path.join(build,'final');
await fs.mkdir(finaldir,{recursive:true});
const repo='https://github.com/bobshenruililin/Laidlaw-Heat-Project';
const sha='b103e96c6761f3409fab6f116c6675b43fdb2ee3';
const refs={
 receipt:`${repo}/blob/${sha}/reports/data_receipt_2026-08-07.md`,
 annual:`${repo}/blob/${sha}/outputs/tables/cvd_descriptive_annual_totals.csv`,
 sensitivity:`${repo}/blob/${sha}/outputs/tables/cvd_trend_depletion_sensitivity.csv`,
 core:`${repo}/blob/${sha}/outputs/release_chd_hf/tables/table2_core_models.csv`,
 diabetes:'https://pubmed.ncbi.nlm.nih.gov/41049877/',
 hypertension:'https://pubmed.ncbi.nlm.nih.gov/40410292/',
 continuity:'https://doi.org/10.1111/dom.70984',
 journal:'https://www.nature.com/natcardiovascres/aims',
 workflows:'https://github.com/EvoScientist/EvoSkills'};
function txt(s,t,x,y,w,h,size=27,bold=false,color=ink){
 let q=s.shapes.add({geometry:'textbox',position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
 q.text=t;q.text.style={typeface:font,fontSize:size,bold,color,autoFit:'none'};return q;
}
function slide(title,ids,extra=''){
 let s=p.slides.add();s.background.fill='#FFFFFF';
 txt(s,title,64,44,1152,95,42,true,navy);
 txt(s,'LAIDLAW  INTERNAL RESEARCH STATE  2 OCT 2026',64,677,900,22,16,false,muted);
 txt(s,`${p.slides.items.length} / 10`,1130,677,86,22,16,false,muted);
 txt(s,`Sources: ${ids.join(', ')}. Links and scientific limits in notes.`,64,641,1152,24,17,false,muted);
 s.speakerNotes.textFrame.setText(ids.map(id=>`${id}: ${refs[id]}`).join('\n')+'\n'+extra);
 return s;
}
function table(s,values,top,height,widths,size=25){
 const t=s.tables.add({rows:values.length,columns:values[0].length,left:64,top,width:1152,height,columnWidths:widths,values});
 t.borders.assign({style:'solid',fill:'#D6DFE2',width:1});
 t.cells.block({row:0,column:0,rowCount:values.length,columnCount:values[0].length}).assign({fill:'#FFFFFF',textStyle:{typeface:font,fontSize:size,color:ink},margins:{left:14,right:14,top:12,bottom:10},anchor:'center'});
 for(let r=0;r<values.length;r++)t.rows[r].height=height/values.length;
 t.cells.block({row:0,column:0,rowCount:1,columnCount:values[0].length}).assign({fill:navy,textStyle:{typeface:font,fontSize:size,bold:true,color:'#FFFFFF'}});
 return t;
}
let s=slide('Research State Briefing',['receipt','core','journal']);
txt(s,'Why did recorded\nhospitalisations change?',64,190,1152,160,54,true,navy);
txt(s,'Evidence-supported manuscript and next-study design',64,407,1152,52,31,false,teal);
txt(s,'Available evidence: count trajectories and exploratory weather models.\nClinical mechanisms, cohort incidence and causal COVID effects remain unresolved.',64,491,1152,105,28);

s=slide('What the present outcome records',['receipt']);
table(s,[['Component','Current evidence','Boundary'],['Population','T2D and/or hypertension diagnosed during 2013-2023','Entry, exits and risk-set construction need query confirmation'],['Event','First recorded hospitalisation after first CHD/HF diagnosis','Admission cause is unavailable'],['Scale','132 territory-month counts per outcome','No linked clinical measurements or eligible person-time']],167,355,[225,457,470],25);
txt(s,'An underlying clinical change, a care-use change or an extraction change\ncan alter the same recorded endpoint.',64,554,1152,76,27,false,teal);

s=slide('Recent studies raise the novelty threshold',['diabetes','hypertension','continuity'],'Youn2025 and Hu2025: abstracts checked only. Yau2026: full main text checked, supplements not checked. Record-specific locators and unresolved definitions appear in literature/covid_novelty_audit_2026-10-02.md. No reported coefficients are imported.');
table(s,[['Prior study','Overlapping contribution','Implication'],['Diabetes, 2025\nHong Kong and Korea','Cardiovascular outcomes, mortality and healthcare use','Another diabetes admissions trend needs a new question'],['Hypertension, 2025\nHong Kong','Cardiovascular outcomes and blood-pressure control','Adding blood pressure alone does not establish novelty'],['Care continuity, 2026\nYau et al.','CHD/HF, clinical covariates and competing death','Later follow-up and clinical linkage already have precedent']],164,379,[272,452,428],25);
txt(s,'Candidate contribution: discriminate disease change from observation change.\nA novelty gate must confirm that contribution before committing to the expanded study.',64,570,1152,66,26,false,teal);

s=slide('Distinct targets require distinct evidence',['receipt','core']);
table(s,[['Target','Required data','Current status'],['Recorded burden','Counts with stable extraction definitions','Available, definitions partly unresolved'],['Cohort incidence','Validated events and eligible person-time','Requires new governed data'],['Changing weather association','Full-series common basis and direct interaction contrast','Not estimated'],['Causal health-system mechanism','Defined intervention and defensible identification assumptions','Not identified']],164,389,[280,452,420],25);
txt(s,'Calendar periods describe context. They do not by themselves define\na treatment, valid comparator or causal intervention.',64,576,1152,63,25,false,teal);

s=slide('Recorded counts declined before 2020',['annual'],'HA_APPROVED_AGGREGATE. Annual index = 100 * count / 2013 count, rounded to six decimals for the editable workbook. No population denominator used. An index compares trajectories, not cohort incidence.');
const raw=await fs.readFile(path.join(root,'figures/covid_period/figure_annual_counts_20261002_source.csv'),'utf8');
const rows=raw.trim().split(/\r?\n/).slice(1).map(line=>{const [outcome,year,total_events]=line.split(',');return{outcome,year,total_events:Number(total_events)};});
const years=rows.filter(r=>r.outcome==='chd').map(r=>r.year);
const series=['chd','hf'].map((o,i)=>{const rs=rows.filter(r=>r.outcome===o);return{name:o.toUpperCase(),values:rs.map(r=>Number((100*r.total_events/rs[0].total_events).toFixed(6))),fill:i?red:teal,line:{fill:i?red:teal,width:3}};});
const chart=s.charts.add('line',{position:{left:64,top:153,width:1152,height:395},title:'Annual recorded first-hospitalisation counts (2013 = 100)',titleTextStyle:{typeface:font,fontSize:24,fill:ink},categories:years,series,hasLegend:true,legend:{position:'bottom',textStyle:{typeface:font,fontSize:24}},lineOptions:{smooth:false},xAxis:{textStyle:{typeface:font,fontSize:22},numberFormatCode:'0'},yAxis:{min:0,max:110,majorUnit:25,numberFormatCode:'0',textStyle:{typeface:font,fontSize:22}},chartFill:'#FFFFFF',plotAreaFill:'#FFFFFF'});
applyPresentationChartFont(chart,{fontFamily:font});
txt(s,'Both series were already near half their 2013 totals by 2019.\nThe 2020 trough and later recovery require a separate explanation.',64,566,1152,68,27);

s=slide('Overlapping windows do not test a period effect',['sensitivity','core']);
table(s,[['Count ratio per five days','2013-2019\n84 months','2013-2023\n132 months'],['HF cold days','1.113 (1.053-1.176)','1.073 (1.006-1.144)'],['CHD cold days','1.036 (1.007-1.067)','0.995 (0.949-1.043)'],['CHD hot nights','1.011 (0.991-1.032)','1.022 (1.002-1.042)']],160,331,[420,366,366],27);
txt(s,'These examples use Newey-West lag-6 intervals. The 84 months are nested\ninside 132, and subsetting changes spline bases and exposure support.',64,514,1152,71,26);
txt(s,'No separate post-period model or formal period-difference test exists.',64,602,1152,30,27,true,teal);

s=slide('Model criticism limits interpretation',['sensitivity','core']);
table(s,[['Check','Observed issue','Consequence'],['Calendar control','HF cold-day interval includes 1 under 8 df and year effects','Baseline interval exclusion is fragile'],['Start-window control','Omitting 24 initial months weakens the HF cold-day estimate','Entry or early extraction remains a rival'],['Covariance and multiplicity','CHD hot nights depends on SE method. All core BH q > 0.19','No protected thermal discovery'],['Design','Nested window changes mix support, trend and period','A common-basis interaction still needs new execution']],165,405,[250,492,410],25);
txt(s,'The complete released panel remains visible. No preferred fit rescues a headline.',64,597,1152,34,25,false,teal);

s=slide('Rivals make different predictions',['receipt','continuity']);
table(s,[['Explanation','Discriminating evidence','Failure mode'],['Improved underlying health','Validated event rates and clinical change beyond selected attendance','Retained attenders alone can create apparent improvement'],['Reduced or delayed care','Contacts, delayed presentation and mortality linkage','Fewer admissions alone cannot distinguish care from disease'],['Changed risk set or recording','Entry, prior events, exits and stable event construction','Counts can move without a change in event propensity'],['Respiratory or thermal context','Matched coverage and formal common-basis contrasts','Adjustment alone does not establish mediation']],162,422,[266,493,393],24);
txt(s,'Multiple explanations may coexist. Severe tests need power to distinguish them.',64,602,1152,27,24,true,teal);

s=slide('The expanded study has a feasibility gate',['receipt','journal','workflows']);
txt(s,'READY NOW',64,166,550,35,25,true,teal);
txt(s,'Exploratory manuscript and source-linked figures\nNovelty and measurement audit\nDraft governed request and rival predictions',64,216,550,170,29);
txt(s,'NOT READY FOR A MECHANISM CLAIM',668,166,548,35,25,true,red);
txt(s,'No new transfer or approved model output\nNo cohort person-time or clinical linkage\nNo independent validation cohort',668,216,548,170,29);
txt(s,'Proceed only if verified fields can separate the explanations and the question\nadds to the closest studies. Otherwise narrow the claim and reconsider journal fit.',64,474,1152,127,29);

s=slide('Next sequence and submission boundary',['journal','workflows']);
const steps=[['1  DATA AND NOVELTY','Review request, verify schema and close the specific novelty question.'],['2  DESIGN FREEZE','Prespecify estimands, rivals, error-detection tests and validation before new fits.'],['3  SECURE EXECUTION','Run in the approved environment. Release reviewed aggregate outputs only.'],['4  INDEPENDENT CRITICISM','Review identifiability, calibration, missingness and discordant results.'],['5  MANUSCRIPT AND VENUE','Complete human ethics and authorship facts, then select the journal from evidence.']];
steps.forEach((r,i)=>{txt(s,r[0],64,158+i*90,1152,30,22,true,teal);txt(s,r[1],64,192+i*90,1152,50,26);});
s.speakerNotes.textFrame.setText('No journal submission, author contact or data-transfer approval follows from this briefing. Nature Cardiovascular Research is a fit benchmark, not an acceptance claim.\n'+refs.journal+'\n'+refs.workflows);

const candidate=path.join(build,'candidate.pptx');
await(await PresentationFile.exportPptx(p)).save(candidate);
for(let i=0;i<p.slides.items.length;i++){
 const blob=await p.export({slide:p.slides.items[i],format:'png',scale:1});
 await fs.writeFile(path.join(build,`slide-${i+1}.png`),new Uint8Array(await blob.arrayBuffer()));
}
const final=path.join(finaldir,`Research_State_Briefing_${Date.now()}.pptx`);
await finalizePresentation({explicitTotalSlideCount:10,requiredNativeTableOwnerSlides:[2,3,4,6,7,8],requiredNativeChartOwnerSlides:[5],materializeLiteralChartWorkbooks:true,workspaceDir:root,candidatePath:candidate,finalPath:final,pythonExecutable:python,integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-heading-fit',...[2,3,4,6,7,8].flatMap(n=>['--require-native-table-slide',String(n)])],fontPolicy:{basis:'design',families:[font]},verifyArtifactToolImport:true,receiptPath:path.join(build,path.basename(final)+'.validation.json')});
await fs.copyFile(final,path.join(root,'reports/auto_research/2026-10-02/Research_State_Briefing.pptx'));
console.log(JSON.stringify({slides:10,final}));
