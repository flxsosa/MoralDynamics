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
	this.init_intro = function() {
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
		if (that.init_intro()) {
			debug("Show STIMULUS");

			// Show video
			video_name = that.introinfo.name,
			$("#intro_slide").attr("src", '/static/videos/' + video_name + '.jpg');

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
		CURRENTVIEW = new Questions()
	};

	// Load the trial html page
	$(".slide").hide();

	// Show the slide
	var that = this;
	$("#intro").fadeIn($c.fade);
	$('#intro_next.next').click(function() {
		that.record_response();
	});


	// Initialize the current trial
	if (this.init_intro()) {
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

		// Create a click counter
		var playClick = 0;
		if (that.init_trial()) {
			debug("Show STIMULUS");

			// Show video
			video_name = that.trialinfo.name,
			$("#video_mp4").attr("src", '/static/videos/avi/' + video_name + '.mp4');
			$("#video_webm").attr("src", '/static/videos/webm' + video_name + '.webm');
			$("#video_ogg").attr("src", '/static/videos/ogg' + video_name + '.ogv');
			$(".stim_video").load()

			$("#play.next").click(function() {
				$(".stim_video").load()
				$('.stim_video').trigger('play');
			});

			// When the play button is cliced, increment a counter
			$("#play").click(function() {
				playClick++;
				// If it's clicked more than twice, enable Continue and disable
				// play button
				if (playClick >= 2) {
	 				$('#play').prop('disabled', true);
	 				playClick = 0;
	 				func();
	 			}
			});
 
            debug($c.questions);
 			var func = function(){
	            // Create the HTML for the question and slider.
	            var html = "";
	            for (var i = 0; i < $c.questions.length; i++) {
	            	// Add in the questions from list in stim.json
	                var q = $c.questions[i].q;
	                html += '<p class=".question">' + q + '</p><div class="s-' + i + '"></div><div class="l-' + i + '"></div><br />';
	            }
	            $('#choices').html(html);
	 
	            // Bulid the sliders for each question
	            for (var i = 0; i < 1; i++) {
	                // Create the sliders
	                $('.s-' + i).slider().on("slidestart", function(event, ui) {
	                    // Show the handle
	                    $(this).find('.ui-slider-handle').show();
	 
	                    // Sum is the number of sliders that have been clicked
	                    var sum = 0;
	                    for (var j = 0; j < $c.questions.length; j++) {
	                        if ($('.s-' + j).find('.ui-slider-handle').is(":visible")) {
	                            sum++;
	                        }
	                    }
	                    // If the number of sliders clicked is equal to the number of sliders
	                    // the user can continue. 
	                    if (sum == $c.questions.length) {
	                        $('#trial_next').prop('disabled', false);
	                    }
	                });
	 
	                // Put labels on the sliders
	                $('.l-' + i).append("<label style='width: 33%'>" + $c.questions[i].l[0] + "</label>");
	            }
	 
	            // Hide all the slider handles 
	            $('.ui-slider-handle').hide();
	 		}
            // Disable button which will be enabled once the sliders are clicked
            $('#trial_next').prop('disabled', true);
            $('#play').prop('disabled', false);

            debug(that.trialinfo);

            // Remove slider after each trial
            $('#choices').html("");
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

		// Record responses to psiturk
		psiTurk.recordTrialData([this.trialinfo.name, question[0], response[0], question[1], response[1], question[2], response[2], ])

		// Increment the state index
		STATE1.set_index(STATE1.index + 1);

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
 *  Questions  *
 *****************/

var Questions = function() {
	var that = this;

	// Show the slide
	$(".slide").hide();
	$("#questions").fadeIn($c.fade);

	//disable button initially
	$('#question_finish').prop('disabled', true);

	//checks whether all questions were answered
	$('.demoQ').change(function() {
		if ($('input[name=q1]:checked').length > 0 &&
			$('input[name=q2]:checked').length > 0 &&
			$('input[name=q3]:checked').length > 0 &&
			$('input[name=q4]:checked').length > 0) 
		{
			// If so, able to submit answers
			$('#question_finish').prop('disabled', false)
		} 
		else {
			// Else, not
			$('#question_finish').prop('disabled', true)
		}
	});

	this.finish = function() {
		debug("Finish test phase");

		// Check if the input answers are correct
		if ($('input[name=q1]:checked').val() =="A" &&
			$('input[name=q2]:checked').val() =="A" &&
			$('input[name=q3]:checked').val() =="A" &&
			$('input[name=q4]:checked').val() =="A") 
		{
			// If so, move into stimuli
			CURRENTVIEW = new TestPhase();
		} 
		else {
			// Else, go back to the introduction
			CURRENTVIEW = new Introduction();
		}
		
	}; 

	$('#question_finish').click(function() {
		that.finish();
	});
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
	} else if (STATE.introduction) {
		CURRENTVIEW = CURR = new Introduction();
	} else if (STATE.questions) {
		CURRENTVIEW = new Questions();
	} else {
		CURRENTVIEW = new TestPhase();
	}
});