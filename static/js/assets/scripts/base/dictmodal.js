const dictmod = new bootstrap.Modal(document.getElementById('dictmod'), {
    keyboard: false
})
var dictmodElem = document.getElementById('dictmod')
dictmodElem.addEventListener('hidden.bs.modal', function () {
    if (document.getElementById("dictionary-content")) document.getElementById("dictionary-content").remove()
})

