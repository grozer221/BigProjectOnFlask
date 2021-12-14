const changeRole = async (e) => {
    e.disabled = true
    const response = await fetch(window.location.protocol + '//' + window.location.host + `/admin/users/updateRole?id=${e.name}&role=${e.value}`, {
        method: 'POST',
        credentials: 'include'
    })
    e.disabled = false
}