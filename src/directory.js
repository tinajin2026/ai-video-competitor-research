const rows=[...document.querySelectorAll('[data-company]')],body=document.getElementById('directory-rows');
function filterDirectory(){const q=document.getElementById('directory-search').value.trim().toLowerCase(),group=document.getElementById('directory-group').value,key=document.getElementById('directory-sort').value;let count=0;
 const sorted=key==='original'?rows:rows.slice().sort((a,b)=>Number(a.dataset.scope!=='site')-Number(b.dataset.scope!=='site')||Number(b.dataset[key])-Number(a.dataset[key]));
 sorted.forEach(row=>{row.hidden=!(row.textContent.toLowerCase().includes(q)&&(group==='all'||row.dataset.group===group));if(!row.hidden)count++;body.append(row);});document.getElementById('directory-count').textContent=count+' 家';document.getElementById('directory-empty').hidden=!!count;}
['directory-search','directory-group','directory-sort'].forEach(id=>document.getElementById(id).addEventListener(id==='directory-search'?'input':'change',filterDirectory));
