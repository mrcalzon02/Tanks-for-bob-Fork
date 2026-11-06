#!/usr/bin/env node

// Rebuild the importable primitive meshes from designs.json; no npm dependencies.

import fs from "node:fs";

import path from "node:path";

import {fileURLToPath} from "node:url";

function f4(x){return (Math.abs(x)<.00005?0:x).toFixed(4)}

function mesh(p){
 const v=[],faces=[];const q=(a,b,c,d)=>{faces.push([a,b,c],[a,c,d])};
 if(p.shape==="box"||p.shape==="beam"){
  let w;
  if(p.shape==="box"){
   const [x,y,z]=p.at,[a,b,c]=p.size;
   w=[[x-a/2,y-b/2,z-c/2],[x+a/2,y-b/2,z-c/2],[x+a/2,y+b/2,z-c/2],[x-a/2,y+b/2,z-c/2],[x-a/2,y-b/2,z+c/2],[x+a/2,y-b/2,z+c/2],[x+a/2,y+b/2,z+c/2],[x-a/2,y+b/2,z+c/2]];
  }else{
   const a=p.p0,b=p.p1,d=b.map((x,i)=>x-a[i]),len=Math.hypot(...d),axis=d.map(x=>x/len),ref=Math.abs(axis[2])<.9?[0,0,1]:[0,1,0];
   const cross=(a,b)=>[a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0]];
   let u=cross(ref,axis),n=Math.hypot(...u);u=u.map(x=>x/n);const k=cross(axis,u);
   let f=[[-1,-1],[1,-1],[1,1],[-1,1]];
   w=[...f.map(([i,j])=>a.map((x,n)=>x+(i*u[n]+j*k[n])*p.width/2)),...f.map(([i,j])=>b.map((x,n)=>x+(i*u[n]+j*k[n])*p.width/2))];
  }
  v.push(...w);q(0,3,2,1);q(4,5,6,7);q(0,1,5,4);q(1,2,6,5);q(2,3,7,6);q(3,0,4,7);
 }else if(p.shape==="roof"){
  const [x,y,z]=p.at,[sx,sy,sz]=p.size;
  v.push([x-sx/2,y-sy/2,z-sz/2],[x-sx/2,y+sy/2,z-sz/2],[x-sx/2,y,z+sz/2],
         [x+sx/2,y-sy/2,z-sz/2],[x+sx/2,y+sy/2,z-sz/2],[x+sx/2,y,z+sz/2]);
  q(0,3,5,2);q(2,5,4,1);q(0,1,4,3);faces.push([0,2,1],[3,4,5]);
 }else if(["cylinder","cone","ring"].includes(p.shape)){
  const n=12,[x,y,z]=p.at,ax=p.axis||"z",h=p.h;
  const pt=(r,off,t)=>{const a=r*Math.cos(t),b=r*Math.sin(t);return ax==="x"?[x+off,y+a,z+b]:ax==="y"?[x+a,y+off,z+b]:[x+a,y+b,z+off]};
  if(p.shape==="ring"){
   for(const [r,off] of [[p.outer,-h/2],[p.outer,h/2],[p.inner,-h/2],[p.inner,h/2]])for(let i=0;i<n;i++)v.push(pt(r,off,2*Math.PI*i/n));
   for(let i=0;i<n;i++){const j=(i+1)%n;q(i,j,n+j,n+i);q(n+i,n+j,3*n+j,3*n+i);q(2*n+j,2*n+i,3*n+i,3*n+j);q(2*n+i,2*n+j,j,i)}
  }else{
   for(let i=0;i<n;i++)v.push(pt(p.r,-h/2,2*Math.PI*i/n));
   for(let i=0;i<n;i++)v.push(pt(p.shape==="cone"?.1*p.r:p.r,h/2,2*Math.PI*i/n));
   const bot=v.length;v.push(pt(0,-h/2,0));const top=v.length;v.push(pt(0,h/2,0));
   for(let i=0;i<n;i++){const j=(i+1)%n;q(i,j,n+j,n+i);faces.push([bot,j,i],[top,n+i,n+j])}
  }
 }else throw Error("unsupported shape "+p.shape);
 if(v.length<3||faces.length===0||v.some(a=>a.some(x=>!Number.isFinite(x))))throw Error("invalid part "+p.label);
 return{v,faces};
}

function obj(model){
 let a=[`# Tanks for Bob primitive mesh: ${model.id}`,"# Blender-importable; X east, Y north, Z up; rough tile scale",`# Sprite reference: ${model.sprite}`,"mtllib survival-materials.mtl",`o ${model.id}`],offset=0,triangles=0;
 for(const p of model.parts){
  const g=mesh(p);a.push(`g ${model.id}_${p.label.replace(/[^a-zA-Z0-9_]+/g,"_")}`,`usemtl ${p.mat}`);
  for(const q of g.v)a.push("v "+q.map(f4).join(" "));
  for(const t of g.faces)a.push("f "+t.map(x=>x+offset+1).join(" "));
  offset+=g.v.length;triangles+=g.faces.length;
 }
 return {content:a.join("\n")+"\n",vertices:offset,triangles};
}

function mtl(materials){
 let lines=["# Prototype material palette; material names preserve editable Blender part groups",""];
 for(const [name,rgb] of Object.entries(materials))lines.push(`newmtl ${name}`,"Ka 0.1000 0.1000 0.1000","Kd "+rgb.map(f4).join(" "),"Ks 0.0300 0.0300 0.0300","Ns 5.0000","d 1.0000","illum 2","");
 return lines.join("\n")+"\n";
}

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

const directory = path.join(root,"models","island-survival");

const manifest = JSON.parse(fs.readFileSync(path.join(directory,"designs.json"),"utf8"));

const target = path.join(directory,"obj");

const check = process.argv.includes("--check");

if (!check) fs.mkdirSync(target,{recursive:true});

let failures=0,verts=0,triangles=0;

function publish(name,text){const file=path.join(target,name); if(check){if(!fs.existsSync(file)||fs.readFileSync(file,"utf8")!==text){console.error("[MODEL-FAIL] "+name);failures++}}else fs.writeFileSync(file,text,"utf8")}

publish("survival-materials.mtl",mtl(manifest.materials));

for(const model of manifest.models){const data=obj(model);publish(model.id+".obj",data.content);verts+=data.vertices;triangles+=data.triangles}

console.log("[MODELS] "+manifest.models.length+" meshes; "+verts+" vertices; "+triangles+" triangles; "+(check?"checked":"generated"));

if(failures)process.exitCode=1;
