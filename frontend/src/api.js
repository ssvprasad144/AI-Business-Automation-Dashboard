const API_BASE=import.meta.env.VITE_API_BASE_URL||"http://127.0.0.1:8000/api";
async function request(path,options={}){const res=await fetch(API_BASE+path,{headers:{"Content-Type":"application/json",...(options.headers||{})},...options});if(!res.ok)throw new Error(`API request failed: ${res.status}`);return res.json();}
export const getDashboard=()=>request("/dashboard/");
export const createWorkflow=(payload)=>request("/workflows/",{method:"POST",body:JSON.stringify(payload)});
export const getWorkflows=()=>request("/workflows/");
export const runWorkflow=(id)=>request(`/workflows/${id}/run/`,{method:"POST"});
export const getActivity=()=>request("/activity/");
