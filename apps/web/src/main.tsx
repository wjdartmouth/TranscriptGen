import React, {useEffect,useState} from 'react';
import {createRoot} from 'react-dom/client';
import './style.css';
type School={id:string;name:string};
type Student={id:string;name:string;grade_level:string};
type Transcript={school:string;student:string;grade_level:string;status:string;grades:{course:string;academic_year:string;grade:string}[]};
function App(){
 const [schools,setSchools]=useState<School[]>([]);
 const [school,setSchool]=useState('');
 const [students,setStudents]=useState<Student[]>([]);
 const [student,setStudent]=useState('');
 const [data,setData]=useState<Transcript|null>(null);
 const [error,setError]=useState('');
 useEffect(()=>{fetch('/api/schools').then(r=>{if(!r.ok)throw Error('Schools unavailable');return r.json()}).then((items:School[])=>{setSchools(items);setSchool(items[0]?.id||'')}).catch(e=>setError(e.message))},[]);
 useEffect(()=>{setStudent('');setData(null);if(!school)return;fetch('/api/schools/'+school+'/students').then(r=>r.json()).then((items:Student[])=>{setStudents(items);setStudent(items[0]?.id||'')}).catch(()=>setError('Student lookup failed'))},[school]);
 useEffect(()=>{setData(null);if(!school||!student)return;fetch('/api/schools/'+school+'/students/'+student+'/transcript').then(r=>r.json()).then(setData).catch(()=>setError('Transcript preview failed'))},[school,student]);
 return <main><header><h1>TranscriptGen</h1><p>Multi-school transcript workspace · Sprint 1 demo</p></header><section className="panel"><h2>Transcript generator</h2><p className="warning">SYNTHETIC DATA ONLY — NOT OFFICIAL</p><div className="fields"><label>School<select value={school} onChange={e=>setSchool(e.target.value)}>{schools.map(s=><option key={s.id} value={s.id}>{s.name}</option>)}</select></label><label>Student<select value={student} onChange={e=>setStudent(e.target.value)}>{students.map(s=><option key={s.id} value={s.id}>{s.name} · Grade {s.grade_level}</option>)}</select></label></div>{error&&<p role="alert">{error}</p>}{data&&<article className="preview"><h2>{data.school}</h2><h3>Sample Academic Transcript</h3><p><strong>{data.status}</strong></p><p>Student: {data.student} · Grade {data.grade_level}</p><table><thead><tr><th>Year</th><th>Course</th><th>Grade</th></tr></thead><tbody>{data.grades.map((g,i)=><tr key={i}><td>{g.academic_year}</td><td>{g.course}</td><td>{g.grade}</td></tr>)}</tbody></table><a className="button" href={'/api/schools/'+school+'/students/'+student+'/transcript.pdf'}>Download sample PDF</a></article>}</section><footer>Not connected to ManageBac. Do not use real student information.</footer></main>
}
createRoot(document.getElementById('root')!).render(<React.StrictMode><App/></React.StrictMode>);
