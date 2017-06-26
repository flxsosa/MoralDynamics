/* task.js
 * 
 * This file holds the main experiment code.
 * 
 * Requires:
 *   config.js
 *   psiturk.js
 *   utils.js
 */

// Create and initialize the experiment configuration object
var $c = new Config(condition, counterbalance);

// Initalize psiturk object
var psiTurk = new PsiTurk(uniqueId, adServerLoc);

// Preload the HTML template pages that we need for the experiment
psiTurk.preloadPages($c.pages);

// Objects to keep track of the current phase and state
var CURRENTVIEW;
var STATE;
var STATE1;

/*************************
 * INSTRUCTIONS         
 *************************/

var Instructions = function() {
	
	console.log("Instructions")
	
	$(".slide").hide();
	var slide = $("#instructions-training-1");
	slide.fadeIn($c.fade);

	slide.find('.next').click(function() {
		CURRENTVIEW = new Introduction();
	});
};

/*****************
 *  Inroduction  *
 *****************/

var Introduction = function() {
	/* Instance variables */
	console.log("Introduction")
	// Information about the current trial
	this.introinfo;
	// The response they gave
	this.response;
	// The number they've gotten correct, so far
	this.num_correct = 0;

	// Initialize a new trial. This is called either at the beginning
	// of a new trial, or if the page is reloaded between trials.
	this.init_trial = function() {
		debug("Initializing trial " + STATE.index);

		// If there are no more trials left, then we are at the end of
		// this phase
		if (STATE.index >= $c.introslides.length) {
			this.finish();
			return false;
		}

		// Load the new trialinfo
		this.introinfo = $c.introslides[STATE.index];

		// Update progress bar
		update_progress(STATE.index, $c.introslides.length);

		return true;
	};

	this.display_stim = function(that) {
		if (that.init_trial()) {
			debug("Show STIMULUS");

			// Show video
			video_name = that.introinfo.name,
			$("#video_mp4").attr("src", '/static/videos/' + video_name + '.jpg');
			//$("#video_webm").attr("src", '/static/videos/' + video_name + '.jpg');
			//$("#video_ogg").attr("src", '/static/videos/' + video_name + '.jpg');
			//$(".stim_video").load()

			$("#play.next").click(function() {
				$(".stim_video").load()
				$('.stim_video').trigger('play');
			});

			debug(that.introinfo);
		}
	};


	// Record a response (this could be either just clicking "start",
	// or actually a choice to the prompt(s))
	this.record_response = function() {
		// TODO MAKE THIS CORRECT!
		var response = [];
		for (var i = 0; i < $c.questions.length; i++) {
			response.push($('.s-' + i).slider('value'));
		}

		var question = $c.questions.map(function(question) {
			return question.type
		});

		psiTurk.recordTrialData([this.introinfo.name, question[0], response[0], question[1], response[1], question[2], response[2], ])

		STATE.set_index(STATE.index + 1);

		// Update the page with the current phase/trial
		this.display_stim(this);
	};

	this.finish = function() {
		debug("Finish Introduction");
		console.log("(Introduction) Printing index: ")
		console.log(STATE.index)
		STATE.set_index(0)

		// Change the page
		CURRENTVIEW = new TestPhase()
	};

	// Load the trial html page
	$(".slide").hide();

	// Show the slide
	var that = this;
	$("#trial").fadeIn($c.fade);
	$('#trial_next.next').click(function() {
		that.record_response();
	});


	// Initialize the current trial
	if (this.init_trial()) {
		// Start the test
		this.display_stim(this);
	};
};

/*****************
 *  TRIALS       *
 *****************/

var TestPhase = function() {
	/* Instance variables */
	console.log("Test phase")
	console.log("Initial State Index: " + STATE1.index)
	// Information about the current trial
	this.trialinfo;
	// The response they gave
	this.response;
	// The number they've gotten correct, so far
	this.num_correct = 0;

	// Initialize a new trial. This is called either at the beginning
	// of a new trial, or if the page is reloaded between trials.
	this.init_trial = function() {
		debug("Initializing trial " + STATE1.index);

		// If there are no more trials left, then we are at the end of
		// this phase
		if (STATE1.index >= $c.trials.length) {
			this.finish();
			return false;
		}

		// Load the new trialinfo
		this.trialinfo = $c.trials[STATE1.index];

		// Update progress bar
		update_progress(STATE1.index, $c.trials.length);

		return true;
	};

	this.display_stim = function(that) {
		if (that.init_trial()) {
			debug("Show STIMULUS");

			// Show video
			video_name = that.trialinfo.name,
			$("#video_mp4").attr("src", '/static/videos/' + video_name + '.jpg');
			//$("#video_webm").attr("src", '/static/videos/' + video_name + '.jpg');
			//$("#video_ogg").attr("src", '/static/videos/' + video_name + '.jpg');
			//$(".stim_video").load()

			$("#play.next").click(function() {
				$(".stim_video").load()
				$('.stim_video').trigger('play');
			});

			debug(that.trialinfo);
		}
	};


	// Record a response (this could be either just clicking "start",
	// or actually a choice to the prompt(s))
	this.record_response = function() {
		// TODO MAKE THIS CORRECT!
		var response = [];
		for (var i = 0; i < $c.questions.length; i++) {
			response.push($('.s-' + i).slider('value'));
		}

		var question = $c.questions.map(function(question) {
			return question.type
		});

		psiTurk.recordTrialData([this.trialinfo.name, question[0], response[0], question[1], response[1], question[2], response[2], ])

		console.log("(Test Phase) Printing index: ")
		console.log(STATE1.index)
		STATE1.set_index(STATE1.index + 1);
		console.log("(Test Phase) Printing index: ")
		console.log(STATE1.index)
		// Update the page with the current phase/trial
		this.display_stim(this);
	};

	this.finish = function() {
		debug("Finish test phase");

		// Change the page
		CURRENTVIEW = new Demographics()
	};

	// Load the trial html page
	$(".slide").hide();

	// Show the slide
	var that = this;
	$("#trial").fadeIn($c.fade);
	$('#trial_next.next').click(function() {
		that.record_response();
	});


	// Initialize the current trial
	if (this.init_trial()) {
		// Start the test
		this.display_stim(this);
	};
};

/*****************
 *  DEMOGRAPHICS*
 *****************/

var Demographics = function() {

	var that = this;

	// Show the slide
	$(".slide").hide();
	$("#demographics").fadeIn($c.fade);

	//disable button initially
	$('#trial_finish').prop('disabled', true);

	//checks whether all questions were answered
	$('.demoQ').change(function() {
		if ($('input[name=sex]:checked').length > 0 &&
			$('input[name=age]').val() != "") {
			$('#trial_finish').prop('disabled', false)
		} else {
			$('#trial_finish').prop('disabled', true)
		}
	});

	// deletes additional values in the number fields 
	$('.numberQ').change(function(e) {
		if ($(e.target).val() > 100) {
			$(e.target).val(100)
		}
	});

	this.finish = function() {
		debug("Finish test phase");

		// Show a page saying that the HIT is resubmitting, and
		// show the error page again if it times out or error
		var resubmit = function() {
			$(".slide").hide();
			$("#resubmit_slide").fadeIn($c.fade);

			var reprompt = setTimeout(prompt_resubmit, 10000);
			psiTurk.saveData({
				success: function() {
					clearInterval(reprompt);
					finish();
				},
				error: prompt_resubmit
			});
		};

		// Prompt them to resubmit the HIT, because it failed the first time
		var prompt_resubmit = function() {
			$("#resubmit_slide").click(resubmit);
			$(".slide").hide();
			$("#submit_error_slide").fadeIn($c.fade);
		};

		// Render a page saying it's submitting
		psiTurk.showPage("submit.html");
		psiTurk.saveData({
			success: psiTurk.completeHIT,
			error: prompt_resubmit
		});
	}; //this.finish function end 

	$('#trial_finish').click(function() {
		var feedback = $('textarea[name = feedback]').val();
		var sex = $('input[name=sex]:checked').val();
		var age = $('input[name=age]').val();

		psiTurk.recordUnstructuredData('feedback', feedback);
		psiTurk.recordUnstructuredData('sex', sex);
		psiTurk.recordUnstructuredData('age', age);
		that.finish();
	});
};

// --------------------------------------------------------------------

/*******************
 * Run Task
 ******************/

$(document).ready(function() {
	// Load the HTML for the trials
	psiTurk.showPage("trial.html");

	// Record various unstructured data
	psiTurk.recordUnstructuredData("condition", condition);
	psiTurk.recordUnstructuredData("counterbalance", counterbalance);
	// psiTurk.recordUnstructuredData("choices", $("#choices").html());

	// Start the experiment
	STATE = new State();
	STATE1 = new State();
	// Begin the experiment phase
	if (STATE.instructions) {
		CURRENTVIEW = new Instructions();
	} else if (STATE.introductions) {
		CURRENTVIEW = new Introduction();
	} else {
		CURRENTVIEW = new TestPhase();
	}
});