function delete_application(id, url)
{
    const reponse = fetch(url, {
        method: 'POST'
    }).then(() => {
        document.getElementById(`app_${id}`).remove();
    }).catch((reason) => {
        console.log(reason);
    });
}

async function add_application(url)
{
    const company_name_val = document.getElementById("CompanyNameIn")?.value;
    const date_applied_val = document.getElementById("DateAppliedIn")?.value;
    const date_response_val = document.getElementById("DateResponseIn")?.value;
    const response_type_val = document.getElementById("ResponseTypeIn")?.value;
    const msg_body = JSON.stringify({
        company_name: company_name_val,
        date_applied: date_applied_val,
        date_response: date_response_val,
        response_type: response_type_val
    });
    const request = new Request(url,
    {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: msg_body
    });
    console.log(request);

    fetch(request).catch((reason) => {
        console.log(reason);
    });
}