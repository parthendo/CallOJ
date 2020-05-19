var begin = 1;
var editor;
// var languageSelected = "java";
function createEditor(name, languag, theme) {
    // find the textarea
    var textarea = document.querySelector("form textarea[name=" + name + "]");
    // var languageSelected = document.querySelector("form select[name=" + language + "]");
    // create ace editor 
    editor = ace.edit();
    editor.setTheme("ace/theme/"+theme);
    editor.session.setMode("ace/mode/"+languag);
    editor.container.style.height = "400px"
    editor.session.setValue(textarea.value)
    // replace textarea with ace
    textarea.parentNode.insertBefore(editor.container, textarea)
    textarea.style.display = "none"
    // find the parent form and add submit event listener
    var form = textarea
    while (form && form.localName != "form") form = form.parentNode
    form.addEventListener("submit", function() {
        // update value of textarea to match value in ace
        textarea.value = editor.getValue()
    }, true)
}
if(begin==1)
{
    createEditor("code","c_cpp","monokai");
    begin=2;
}
// createEditor("code","c", "monokai")
// var languageSelected = document.querySelector("form select[name=" + language + "]");
// function myfun(choice){
//    var languageSelected=choice;
//    createEditor("code",choice, "monokai")
//    document.getElementById("demo").innerHTML = choice;
//  }
 $('#language').on('change', function(){
   
  var newLanguage = $(this).val();
  if(newLanguage.localeCompare("JAVA8")==0)
  {
    newLanguage = "java";
    // document.getElementById("demo").innerHTML = newLanguage
  }
  if(newLanguage.localeCompare("C")==0 || newLanguage.localeCompare("C11")==0 || newLanguage.localeCompare("CPP03")==0 || newLanguage.localeCompare("CPP11")==0 || newLanguage.localeCompare("CPP14")==0  || newLanguage.localeCompare("CPP17")==0 )
  {
    newLanguage = "c_cpp";
    // document.getElementById("demo").innerHTML = newLanguage
  }
  if(newLanguage.localeCompare("PY2")==0 || newLanguage.localeCompare("PY3")==0)
  {
    newLanguage = "python";
    // document.getElementById("demo").innerHTML = newLanguage
  }
  if(newLanguage.localeCompare("PERL")==0)
  {
    newLanguage = "perl";
    // document.getElementById("demo").innerHTML = newLanguage
  }
  
  editor.session.setMode({
  path: "ace/mode/" + newLanguage,
  v: Date.now()});
  });

  $('#editorTheme').on('change', function(){
   
   var newTheme = $(this).val();
  //  document.getElementById("demo").innerHTML = newTheme;         
   editor.setTheme("ace/theme/" + newTheme);
   });
