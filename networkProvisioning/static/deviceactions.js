async function getShowVersion(btn) {
    alert('Dette vil trigge funksjonen getShowVersion i static/deviceActions. ' +
        'Dette vil igjen POSTE til /actions med aksjon, hostname og ip_addr som params. ' +
        'Actions URL er definert i urls.py og views.py. I actions-funksjonen i views.py trigges til slutt python-scriptet som skal ' +
        'utføre oppgaven. I dette tilfellet logge på ruter og kjøre show version og så leverer resultatet tilbake ' +
        'i form av JSON. Jeg liker å legge alle tilgjengelige script i en python dictionary som peker på funksjonen som bestilles. ' +
        'Selve python-scriptene legges under scripts-katalogen. Her ender vi ofte opp med et hav av script')

    const hostName = btn.closest('tr').querySelector('[id$=hostname]').value
    const ipAddr = btn.closest('tr').querySelector('[id$=loopback_ip]').value

    data = {
        'action': 'showVersion',
        'args': [hostName, ipAddr],
    }
    const result = await getAction(data)
    alert('Under ser du resultatet av show_version-funksjonen som er definert i scripts.actions som da ble trigget ' +
        'av å klikke på denne knappen : \n\n'+result.result)
}
async function getAction(data) {
        const response = await fetch('/actions/', {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "credentials": "include",
        },
        body: JSON.stringify(data),
    });
    return response.json()
}