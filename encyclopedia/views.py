from django.shortcuts import render
from django.http import Http404  
from django import forms
from . import util
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from numpy import random
import markdown2




class SearchForm(forms.Form):
	search = forms.CharField(label = "Nueva Busqueda")

class newEntryTitle(forms.Form):
	title = forms.CharField(label = "Título")

class EditPage(forms.Form):
	content = forms.CharField(widget = forms.Textarea)


# View for index. Get all entries in a list.
def index(request):
	if request.method == "GET":
		    return render(request, "encyclopedia/index.html", {
		        "entries": util.list_entries(), "form": SearchForm()
		    })


# EntryPage 
def entrypage(request, entry):

	# If entry exist render int
	if util.get_entry(entry):
		titles = str(entry)
		entrie = str(util.get_entry(entry))
		entrie = markdown2.markdown(entrie)
		return render(request, "encyclopedia/entrypage.html", { "titles":titles, "entrie":entrie, "form": SearchForm()})


	# If entry not exist
	raise Http404("Entry doesn't exist")



#  Search for a entrie
def search(request):
	if request.method == "POST":
		form = SearchForm(request.POST)
		if form.is_valid():
			busqueda = form.cleaned_data["search"]
			busqueda = busqueda.casefold()
			userinput = str(busqueda)
			entry = util.get_entry(userinput)
			# If there are a perfect match
			if entry is not None:
				entrie = markdown2.markdown(entry)
				return render(request, "encyclopedia/entrypage.html", {
					"entrie": entrie, "titles": userinput, "form": SearchForm()
					})

			else:
				abc = []				
				for entrada in util.list_entries():
					absec = str(entrada).casefold()
					# If there are a list of results
					if userinput in absec:
						abc.append(entrada)
						print(abc)
						print(f"esta es la lista:{abc}")

				abclength = int(len(abc))
				if len(abc) > 0:
					return render(request, "encyclopedia/search.html", {
						"abc": abc, "form": SearchForm()
						})


				# If there are no results
				else:
					message = "Results not found"
					return render(request, "encyclopedia/search.html", {
						"abc": abc, "message":message, "form": SearchForm()
						})	



		else:
	 	   message = "Invalid form"
	 	   return render(request, "encyclopedia/layout.html", {
	    	"form": SearchForm(), "message":message	
	    	})

	else:
	 	   return render(request, "encyclopedia/layout.html", {
	    	"form": SearchForm()
	    	})


# Create a new entrie
def newpage(request):
	if request.method == "POST":
		form = newEntryTitle(request.POST)
		if form.is_valid():
			title = str(form.cleaned_data["title"])
			contenido = str(request.POST.get("contenido"))
			entry = util.get_entry(title)

			# If entry already exists
			if entry is not None:
				message = "Entry already exists"
				return render(request, "encyclopedia/newpage.html", {
					"newtitle": newEntryTitle(), "form": SearchForm(), "message" : message
					})

			# If entry doesn't exist: save entry.
			else:
				util.save_entry(title, contenido)
				contenido = markdown2.markdown(contenido)
				return render(request, "encyclopedia/entrypage.html", {
					"titles":title, "entrie":contenido, "form":SearchForm()
					})



		else:
			return render(request, "encyclopedia/newpage.html", {
				"newtitle": newEntryTitle(), "form": SearchForm()
				})

	else:
		return render(request, "encyclopedia/newpage.html", {
			"newtitle": newEntryTitle(), "form": SearchForm()
			})



# Edit Page
def editpage(request, entry):

	if request.method == "POST":
		form = EditPage(request.POST)
		# If form is valid: save entry
		if form.is_valid():
			titulo = entry
			contenido = form.cleaned_data["content"]
			util.save_entry(titulo, contenido)
			contenido = markdown2.markdown(contenido)
			return render(request, "encyclopedia/entrypage.html", {
					"titles": titulo, "entrie": contenido, "form": SearchForm()
					})

		# If form isn't valid: render edit page
		else:
			entrie = util.get_entry(entry)
			prepopulatedForm = {'content': entrie}
			editform = EditPage(prepopulatedForm)
			return render(request, "encyclopedia/editpage.html", {
				"title":entry, "editform": editform, "form": SearchForm()
				})



	# If request method is get: render edit page
	else:
		entrie = util.get_entry(entry)
		prepopulatedForm = {'content': entrie}
		editform = EditPage(prepopulatedForm)
		return render(request, "encyclopedia/editpage.html", {
			"title":entry, "editform": editform, "form": SearchForm()
			})


# Random page
def randompage(request):

	allentries = util.list_entries()

	contenedor = []
	for i in range(len(allentries)):
		contenedor.append(i)

	contenedor2 = []
	for m in range(len(allentries)):
		m = 1/(len(allentries))
		contenedor2.append(m)


	toke = random.choice(contenedor, p=contenedor2 , size=(1))
	toke = int(toke)

	print(f"contenedor: {contenedor}")
	print(f"contenedor2: {contenedor2}")
	print(f"toke:{toke}")

	title = allentries[toke]
	entrie = markdown2.markdown(util.get_entry(title))

	return render(request, "encyclopedia/entrypage.html", {
		"titles": title, "entrie": entrie, "form": SearchForm()
		})
	
