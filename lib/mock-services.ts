export const wait=(ms=700)=>new Promise<void>(r=>setTimeout(r,ms));
export async function extractDocuments(){await wait(1300);return {fields:7}}
export async function verifyField(id:string){await wait(250);return {id,status:'VERIFIED'}}
export async function resolveConflict(value:string){await wait(300);return {value,status:'VERIFIED'}}
export async function generateSupplierRequest(){await wait(650);return {id:'REQ-1048'}}
export async function simulateSupplierResponse(){await wait(1400);return {documents:['LeatherOrigin_L18.pdf','REACH_L18_2026.pdf']}}
export async function generatePassport(){await wait(500);return {id:'DPP-S-042'}}
export async function publishPassport(){await wait(700);return {status:'LIVE'}}
