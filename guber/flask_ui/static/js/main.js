function autofill(){
    var x = document.getElementById('policy').value;
    if(x==0)
    {
        document.getElementById('proposal').value= '0';
        document.getElementById('risky').value= '0';
    }
}