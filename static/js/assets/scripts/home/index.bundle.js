(()=>{var e={178:()=>{document.getElementById("subh"),document.querySelector("main")&&document.querySelector("main"),document.addEventListener("dblclick",(function(){if(window.getSelection){var n=window.getSelection().toString(),o=[".",",",":",";","!","?","%","/","<",">","&","#",'"',"{","}","(",")","@","[","]"," ","⭐"];for(char of n)o.includes(char)&&(n=n.replace(char,""));n.length>0&&dictmod.show()}!o.includes(n)&&n.length>0&&n.length<27&&fetch(prde,{method:"POST",headers:{"Content-Type":"application/x-www-form-urlencoded;charset=UTF-8","X-CSRFToken":csrftoken},body:JSON.stringify(n)}).then((async o=>{if(!o.ok){const e=await o.text();throw new Error(e)}{var d=JSON.parse(o.headers.get("definition"));document.getElementById("dictionary-content")&&document.getElementById("dictionary-content").remove(),t.innerHTML="";let a=document.createElement("div");if(a.id="dictionary-content",divTitleContent=document.createTextNode(`${n.charAt(0).toUpperCase()+n.slice(1)}`),t.appendChild(divTitleContent),Object.keys(d).includes("no-result"))document.createElement("p"),pContent=document.createTextNode("No Definition found."),a.appendChild(pContent);else for(const[e,t]of Object.entries(d))if(Object.keys(t).length>0){(r=document.createElement("ul")).className="title";var r,c=document.createTextNode(`${e}`);(i=document.createElement("li")).appendChild(c),r.appendChild(i),a.appendChild(r),(r=document.createElement("ul")).className="def";for(const[e,n]of Object.entries(t)){let e=document.createTextNode(`${n}`);var i;(i=document.createElement("li")).appendChild(e),r.appendChild(i),a.appendChild(r)}}e.appendChild(a)}}))}));var e=document.getElementById("dictionary"),t=document.getElementById("dictionary-title")}},t={};function n(o){var d=t[o];if(void 0!==d)return d.exports;var r=t[o]={exports:{}};return e[o](r,r.exports,n),r.exports}n.n=e=>{var t=e&&e.__esModule?()=>e.default:()=>e;return n.d(t,{a:t}),t},n.d=(e,t)=>{for(var o in t)n.o(t,o)&&!n.o(e,o)&&Object.defineProperty(e,o,{enumerable:!0,get:t[o]})},n.o=(e,t)=>Object.prototype.hasOwnProperty.call(e,t),(()=>{"use strict";n(178)})()})();