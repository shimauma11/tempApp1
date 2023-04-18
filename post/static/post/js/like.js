const getCookie = name => {
    if (document.cookie && document.cookie !== '') {
        for (const cookie of document.cookie.split(';')) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) {
                return decodeURIComponent(value);
            }
        }
    }
};

const csrftoken = getCookie('csrftoken');

async function likeFunc(event) {
    event.preventDefault();
    const el = event.target;
    const id = el.dataset.id;
    let url = "";
    if (el.dataset.is_liked == "true") {
        url = "/post/" + id + "/unlike/";
    } else {
        url = "/post/" + id + "/like/";
    }
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
                'X-CSRFToken': csrftoken,
            },
        })

        if (!response.ok) {
            switch (response.status) {
                case 400:
                    throw new Error('400 error');
                case 401:
                    throw new Error('401 error');
                case 404:
                    throw new Error('404 error');
                case 500:
                    throw new Error('500 error');
                default:
                    throw new Error('something error');
            }
        }

        const data = await response.json();

        if (el.dataset.is_liked == "true") {
            el.dataset.is_liked = "false";
        } else {
            el.dataset.is_liked = "true";
        }
        el.textContent = "いいね: " + String(data.like_count);
    } catch (error) {
        console.log(error);
    }
};
