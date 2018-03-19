  const addItems = document.querySelector('.add-items');
  const removeItemsButton = document.querySelector('.remove-items');
  const doneShoppingButton = document.querySelector('.done-shopping');
  const submitToDBButton = document.querySelector('.submit-to-db');
  const itemsList = document.querySelector('.items');
  const urlRemote = '';
  const urlLocal = 'http://127.0.0.1:5000/';

  //for debug, change to local
  const curURL = urlRemote;

  let items = [];
  getLatestList();

  function getLatestList(){
          let returnList =[];
          let request = new Request(curURL+'getLatest',
				        {method:'get'});

          fetch(request).then(function(response) {
	             return response.json();
	           }).then(function(jsonResponse) {
		              console.log(jsonResponse.length);
		             for (var i = 0; i < jsonResponse.length; i++) {
				               console.log(jsonResponse[i]['S']);
				               const item = {
						                   text: jsonResponse[i]['S'],
						                   done: false,
						                   ListGUID: 'latest'
						                 };
				               addItemToListAndLocalStorage(item)
				       }
		           }).catch(function(err) {
			             //todo: this doesn't seem to work...
			             Error :('error')
			           });

          //TODO: This isn't how this should work...
          return [];// returnList;// || JSON.parse(localStorage.getItem('items')) ||  [];
        }

  function addItemFromField(e) {
          e.preventDefault();  //prevent page from reloading
          const text = (this.querySelector('[name=item]')).value;
          const item = {
	            text,
	            done: false,
	            ListGUID: 'latest'
	          };
          addItemToListAndLocalStorage(item);
          saveToDB();
          this.reset();
        }

  function addItemToListAndLocalStorage(item){
          items.push(item);
          localStorage.setItem('items', JSON.stringify(items));
          populateList(items, itemsList);
        }

  function doneShopping() {
          sendPostRequest('doneShopping', "Done Shopping");
        }
  function saveToDB() {
          sendPostRequest('postList', 'Save To Database')
        }

  function sendPostRequest(URLRoute, errorMessage)
  {
          var request = new Request(curURL+URLRoute,
				        {
					          method: 'POST',
					          headers: new Headers({
						      "content-type":"application/json"
						      }),
					          dataType: 'json',
					          body: JSON.stringify(items)
					        });

          fetch(request).then(function(response) {

	            if(response.ok) {
			        return response.json();
			      }
	           }).catch(function(err) {
		             alert("Error: " + err + 'Click '+ buttonName +' to try again.');
		           });
        }

  function moveItemUpInList(button) {
          const index = parseInt(button.dataset.index);
          if(index === 0) return; //don't do anything if it is already the top item
          swapTwoListItems(index, index-1)
        }

  function moveItemDownInList(button) {
          const index = parseInt(button.dataset.index);
          if(index === items.length-1) return; //don't do anything if it is the last item
          swapTwoListItems(index, index+1);
        }

  function swapTwoListItems(a, b){
          var temp = items[b];
          items[b] = items[a];
          items[a] = temp;
          localStorage.setItem('items', JSON.stringify(items));
          populateList(items, itemsList);
        }

  function removeItemsFromList() {
          //get a list of items not marked done
          var uncheckedItems = items.filter(function(item)
					        {
						          return !item.done;
						        });
          if(uncheckedItems.length != items.length)
	          {
		            items = uncheckedItems;
		            localStorage.setItem('items', JSON.stringify(items));
		            populateList(items, itemsList);
		          }
          saveToDB();
  }

  function populateList(items = [], itemsList) {
          itemsList.innerHTML = items.map((item, i) => {
	            return `
	              <li>
		            <input type="checkbox" data-index=${i} id="item${i}" ${item.done ? 'checked' : ''} />
		            <label for="item${i}">${item.text}</label>
		            <input type="button" data-index=${i} onclick=moveItemUpInList(this) value="Up">
		            <input type="button" data-index=${i} onclick=moveItemDownInList(this) value="Down">
		          </li>
		        `;
	          }).join('');
        }

  function toggleDone(e) {
          if (e.target.type != 'checkbox') return; // skip this unless it's an input
          const el = e.target;
          const index = el.dataset.index;
          items[index].done = !items[index].done;
          localStorage.setItem('items', JSON.stringify(items));
          populateList(items, itemsList);
        }

window.onload = function () {
  addItems.addEventListener('submit', addItemFromField);
  removeItemsButton.addEventListener('click', removeItemsFromList);
  doneShoppingButton.addEventListener('click', doneShopping);
  submitToDBButton.addEventListener('click', saveToDB);
  itemsList.addEventListener('click', toggleDone);
}
