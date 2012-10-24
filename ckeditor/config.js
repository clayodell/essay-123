/*
Copyright (c) 2003-2012, CKSource - Frederico Knabben. All rights reserved.
For licensing, see LICENSE.html or http://ckeditor.com/license
*/

CKEDITOR.editorConfig = function( config )
{
	// Define changes to default configuration here. For example:
		config.toolbar = 'MyToolbar';
		config.language = 'en';
		config.toolbar_MyToolbar =
			[
				{ name: 'clipboard', items : [ 'Cut','Copy','Paste','PasteText','-','Undo','Redo' ] },
				{ name: 'editing', items : [ 'Find','Replace','-','SelectAll' ] },
		                '/',
				{ name: 'styles', items : [ 'Styles','Format' ] },
				{ name: 'basicstyles', items : [ 'Bold','Italic','Strike','-','RemoveFormat' ] },
				{ name: 'paragraph', items : [ 'NumberedList','BulletedList','-','Outdent','Indent','-','Blockquote' ] },
				{ name: 'links', items : [ 'Link','Unlink','Anchor' ] },
				{ name: 'tools', items : [ 'Maximize'] }
			];
};
