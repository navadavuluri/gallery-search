
/**
 *Photo model 
 */
var Photo = Backbone.Model.extend({
	url: '/upload',
	defaults: { 
		about: 'description',
		image_url: 'jpeg',
		id: null,
		addr: null,
		lat: '323',
		lon: '323'
	}
});



/**
 * PhotoCollection: A collection of Photo items 
 */
var PhotoCollection = Backbone.Collection.extend({
	photos: null,
    model: Photo, 
	parse: function(data) {
		return data;
	},
	initialize: function(data) {
		this.photos = data.collection;
		return data.collection;
	}
});

/**
 * IndexView: The default view seen when opening up the application 
 */
var IndexView = Backbone.View.extend({
    el: $('#main'),
    indexTemplate: $("#indexTmpl").template(),

    render: function() {
        var sg = this;
        
        this.el.fadeOut('fast', function() {
        sg.el.empty();
        $.tmpl(sg.indexTemplate, sg.model).appendTo(sg.el);
        sg.el.fadeIn('fast');
        });
        return this;
    }

});

/**
 *UploadView
 */
var UploadView = Backbone.View.extend({
    el: $('#main'),
    uploadTemplate: $("#uploadTmpl").template(),
    events: {
    	'submit form' : 'uploadFile'
    },

    uploadFile: function(event) {
		var values = {};
		var newPhoto = new Photo();

    	if(event){ event.preventDefault(); }

    	_.each(this.$('form').serializeArray(), function(input){
      	 values[ input.name ] = input.value;
    	})

    	newPhoto.save(values, { iframe: true,
                              files: this.$('form :file'),
                              data: values });
    },

	render: function() {
        var sg = this;
        
        this.el.fadeOut('fast', function() {
        sg.el.empty();
        $.tmpl(sg.uploadTemplate, sg.model).appendTo(sg.el);
        sg.el.fadeIn('fast');
        });
        return this;
    }

});

/**
 *SearchView
 */
var SearchView = Backbone.View.extend({
    el: $('#main'),
    searchTemplate: $("#searchTmpl").template(),
    events: {
    	'submit form' : 'searchPhotos'
    },

    searchPhotos: function(event) {//on form submit
		var values = [];

    	if(event){ event.preventDefault(); }

	values = this.$('form').serializeArray()
            $.ajax({//first convert address to lat and lon
                url: 'http://maps.googleapis.com/maps/api/geocode/json',
                data: {
			sensor: false,
			address: values[0]['value']
		},
                success: function(data) {
		    $.ajax({
                	url: '/photos',//call GET with lat, lon and distance info
			type: "GET",
	                data: { 
				lat: data.results[0]['geometry']['location']['lat'],
				lon: data.results[0]['geometry']['location']['lng'],
				distance_mi: values[1]['value']
	                },
	                success: function(data) {
                   		var c = new PhotoCollection(data);
                    		index = new IndexView({model: c.photos});
                    		Backbone.history.loadUrl();
        			index.render();
	                }
	            });

                }
            });
    },

	render: function() {
        var sg = this;
        
        this.el.fadeOut('fast', function() {
        sg.el.empty();
        $.tmpl(sg.searchTemplate, sg.model).appendTo(sg.el);
        sg.el.fadeIn('fast');
        });
        return this;
    }


});



/**
 * Gallery controller 
 */
var Gallery = Backbone.Controller.extend({
    _index: null,
    _photos: null,
    _album :null,
    _uploadPhoto: null,
	_subalbums:null,
	_subphotos:null,
	_data:null,
	_photosview:null,
	_currentsub:null,

    routes: {
        "": "index",
	"upload":"uploadPhoto",
	"search":"searchPhoto"
    },

    initialize: function(options) {
    },


    index: function() {
        var ws = this;
	        if (this._index === null){
            $.ajax({
                url: '/photos',
                dataType: 'json',
                data: {},
                success: function(data) {
                    ws._data = data;
                    var c = new PhotoCollection(data);
                    ws._index = new IndexView({model: c.photos});
                    Backbone.history.loadUrl();
        			ws._index.render();
                }
            });
        }
    },

    uploadPhoto: function() {
    	this._uploadPhoto = new UploadView();
	this._uploadPhoto.render();

    },

    searchPhoto: function() {
	this._searchPhoto = new SearchView();
	this._searchPhoto.render();

    }
});


gallery = new Gallery();
Backbone.history.start();

