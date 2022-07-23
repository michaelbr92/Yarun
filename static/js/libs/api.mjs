const API_ROOT = "http://localhost:8000";
const API_PREFIX = `${API_ROOT}/api/v1`;
export function API(endpoint) {
    return `${API_PREFIX}${endpoint}`;
}

export async function getAPI(endpoint, query = {}) {
    let raw = await fetch(API(endpoint) + "?" + new URLSearchParams(query));
    return await raw.json();
}

export async function postAPI(endpoint, { query = {}, data = {} } = {}) {
    let raw = await fetch(API(endpoint) + "?" + new URLSearchParams(query), {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
    });
    return await raw.json();
}
