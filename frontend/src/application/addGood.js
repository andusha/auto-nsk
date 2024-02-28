import '../styles/addGood.scss';

$(document).ready(function() {
    var $eventSelect = $('.select');
    $eventSelect.select2(
        {
            placeholder: "Выберите вид товара",
            tags: true
        }
    )


    const selectInput = document.getElementById('select_input');
    const nodeArr = [document.getElementById('photo'),
                     document.getElementById('brand_title'),
                     document.getElementById('article'),
                     document.getElementById('manufacturer'),
    ]

	$eventSelect.on("select2:select", function (e) { 
        selectInput.value = e.params.data.id
        if (!isNaN(parseInt(e.params.data.id))) {
            nodeArr.forEach((elem) => {
                if(elem.id !== 'photo'){
                    elem.value = 'Зарезервирован'
                    elem.readOnly = true
                } else elem.disabled = true
            })
            document.getElementById('add-attribute-button').disabled = true
        }
    });

	var readURL = function(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('.profile-pic').attr('src', e.target.result);
            }
    
            reader.readAsDataURL(input.files[0]);
        }
    }
   
    $(".file-upload").on('change', function(){
        readURL(this);
    });
    
    $(".upload-button").on('click', function() {
       $(".file-upload").click();
    });


    let addAttributesFieldBtn = document.getElementById('add-attribute-button');
    addAttributesFieldBtn.addEventListener('click', function(e){
        e.preventDefault();
        let allAttributesFieldWrapper = document.getElementById('attributes');
        let allAttributesField = allAttributesFieldWrapper.getElementsByTagName('input');
        let AttributeInputIds = [-1]
        for(let i = 0; i < allAttributesField.length; i++) {
            if (!isNaN(parseInt(allAttributesField[i].name.split('-')[1]))){
                AttributeInputIds.push(parseInt(allAttributesField[i].name.split('-')[1]));
                console.log(allAttributesField[i], Math.max(...AttributeInputIds))
            }
        }
        let newFieldName = `attributes-${Math.max(...AttributeInputIds) + 1}-attribute`;
        let newFieldName2 = `attributes-${Math.max(...AttributeInputIds) + 1}-value`;
        allAttributesFieldWrapper.insertAdjacentHTML('beforeend',`
        <li class="w-full flex justify-between items-center py-2"><input id="${newFieldName}" name="${newFieldName}" type="text" value="" placeholder="Атрибут"
         class="w-1/2 md:w-fit bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#ff0000] focus:border-[#ff0000] block p-2.5">
            <input id="${newFieldName2}" name="${newFieldName2}" type="text" value="" placeholder="Значение"
            class="w-1/2 md:w-fit bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#ff0000] focus:border-[#ff0000] block p-2.5">
        </li> `);
    }); 
});
