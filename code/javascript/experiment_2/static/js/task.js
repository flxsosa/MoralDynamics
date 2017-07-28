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

/*************************
 * INSTRUCTIONS         
 *************************/

var Instructions = function() {
	
	console.log("Instructions")
	
	$(".slide").hide();
	$(".slide_trial").hide();
	var slide = $("#instructions-training-1");
	slide.fadeIn($c.fade);

	slide.find('.next').click(function() {
		CURRENTVIEW = new Introduction();
	});
};

/*****************
 *  Inroduction  *
 *****************/
var slideNumber = 0;

var Introduction = function() {
	// Information about the current trial
	this.introinfo;
	this.otherinfo;
	var count = 0;

	// Slide number user is one

	// Initialize a new trial. This is called either at the beginning
	// of a new trial, or if the page is reloaded between trials.
	this.init_intro = function() {
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
			// Show video and increment slide number
			slideNumber++;
			console.log("What the other is")
			console.log(slideNumber)
			video_name = that.introinfo.name,
			
			$("#intro_slide").attr("src", '/static/images/' + video_name + '.png');
			
			this.otherinfo = $c.trials[0];
			
			if (slideNumber == 2 || slideNumber == 3 || slideNumber == 4) {
				this.otherinfo=$c.introvids[count];
				count++;

				var html = "";
				// Add in the questions from list in stim.json
				html += '<video loop autoplay class="intro_video" width="600" id="vid"><source src="" id="video_mp4"><source src="" id="video_webm"><source src="" id="video_ogg"></video>';
				video_name = that.otherinfo.name,
				$('#some').html(html);
				$("#video_mp4").attr("src", '/static/videos/mp4/' + video_name + '.mp4');
				$("#video_webm").attr("src", '/static/videos/webm' + video_name + '.webm');
				$("#video_ogg").attr("src", '/static/videos/ogg' + video_name + '.ogv');
				$(".intro_video").load()
				$(".intro_video").load()
				$('.intro_video').trigger('play');
			}
		}
	};

	this.finish = function() {
		slideNumber = 0;
		console.log("Slide Number")
		console.log(slideNumber);
		STATE.set_index(0);
		// Change the page
		CURRENTVIEW = new Questions();
	};

	// Load the trial html page
	$(".slide").hide();
	$(".slide_trial").hide();

	// Show the slide
	var that = this;
	$("#intro").fadeIn($c.fade);
	$('#intro_next.next').click(function() {
		$('#some').html("");
		STATE.set_index(STATE.index + 1);
		// Update the page with the current phase/trial
		that.display_stim(that);
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
	// Information about the current trial
	this.trialinfo;
	// The response they gave
	this.response;
	// The number they've gotten correct, so far
	this.num_correct = 0;

	// Initialize a new trial. This is called either at the beginning
	// of a new trial, or if the page is reloaded between trials.
	this.init_trial = function() {
		// If there are no more trials left, then we are at the end of
		// this phase
		if (STATE.index >= $c.trials.length) {
			this.finish();
			return false;
		}

		// Load the new trialinfo
		this.trialinfo = $c.trials[STATE.index];

		// Update progress bar
		update_progress1(STATE.index, $c.trials.length);

		return true;
	};

	this.display_stim = function(that) {
		// Create a click counter for the play button
		var playClick = 0;
		$('document').ready(function(){
			// Create the sliders
			var html = "";
			// Add in the questions from list in stim.json
			var q = $c.questions[0].q;
			html += '<p class=".question">' + q + '</p><input class="trialQ" name="A" type="radio" value="A"><b>A</b><input class="trialQ" name="A" type="radio" value="B"><b>B</b><br/>';
			$('#choices').html(html);
		});	
		// Create html and build sliders
		
		if (that.init_trial()) {
			// Load and show video
			$('#play1').prop('disabled', false);
			$('#play2').prop('disabled', false);
			video_pair = that.trialinfo.pair
			video_1 = video_pair[0]
			video_2 = video_pair[1]
			$("#video_mp41").attr("src", '/static/videos/mp4/' + video_1 + '.mp4');
			$("#video_webm1").attr("src", '/static/videos/webm/' + video_1 + '.webm');
			$("#video_ogg1").attr("src", '/static/videos/ogv/' + video_1 + '.ogv');
			$("#vid1").load()
			$("#play1.next").click(function() {
				$("#vid1").load()
				$('#vid1').trigger('play');
			});

			$("#video_mp42").attr("src", '/static/videos/mp4/' + video_2 + '.mp4');
			$("#video_webm2").attr("src", '/static/videos/webm/' + video_2 + '.webm');
			$("#video_ogg2").attr("src", '/static/videos/ogv/' + video_2 + '.ogv');
			$("#vid2").load()
			$("#play2.next").click(function() {
				$("#vid2").load()
				$('#vid2').trigger('play');
			});
			
			// Watch for video being played to end and enable play button when done
			// if it's been clicked less than twice
			document.getElementById('vid1').addEventListener('ended',function(e) {
				$('#play1').prop('disabled', false);	
				
			},false);
			document.getElementById('vid2').addEventListener('ended',function(e) {
				$('#play2').prop('disabled', false);
			},false);

			

			// Disable button which will be enabled once the sliders are clicked
			$('#trial_next').prop('disabled', true);
			//$('#trial_next').hide();
			// When the continue button is clicked, reset playClick counter
			$('#trial_next').on('click', function(){
				record_response();
				$('#play1').prop('disabled', false);
				$('#play2').prop('disabled', false);
			});

			// Enable play video button at first
			$('#play').prop('disabled', false);
			
			// When the button is clicked, disable button till end of video
			$('#play1').on('click', function() {
				//playClick++;
				$('#play1').prop('disabled', true);
			});

			$('#play2').on('click', function() {
				//playClick++;
				$('#play2').prop('disabled', true);
			});
			// Remove slider after each trial
			$('.trialQ').change(function() {
				$('#trial_next').prop('disabled', false);
			});
		}
	};

	// Record a response (this could be either just clicking "start",
	// or actually a choice to the prompt(s))
	this.record_response = function() {
		response = $('input[name=A]:checked').val();

		var data = {
			clip: this.trialinfo.pair,
			rating: response
		}

		// Record responses to psiturk
		psiTurk.recordTrialData(data)

		// Increment the state index
		STATE.set_index(STATE.index + 1);

		// Update the page with the current phase/trial
		this.display_stim(this);
	};

	this.finish = function() {
		STATE.set_index(0);
		// Change the page
		CURRENTVIEW = new Demographics()
	};

	// Load the trial html page
	$(".slide").hide();
	$(".slide_trial").hide();

	// Show the slide
	var that = this;
	$("#trial").fadeIn($c.fade);
	$('#trial_next.next').click(function() {
		$('#play').show();
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
	$(".slide_trial").hide();
	$("#questions").fadeIn($c.fade);

	//disable button initially
	$('#question_finish').prop('disabled', true);

	//checks whether all questions were answered
	$('.demoQ').change(function() {
		if ($('input[name=q1]:checked').length > 0 &&
			$('input[name=q2]:checked').length > 0 &&
			$('input[name=q3]:checked').length > 0) 
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
		// Check if the input answers are correct
		if ($('input[name=q1]:checked').val() == "A" &&
			$('input[name=q2]:checked').val() == "B" &&
			$('input[name=q3]:checked').val() == "B") 
		{
			STATE.set_index(0);
			// If so, move into stimuli
			CURRENTVIEW = new TestPhase();
		} 
		else {
			STATE.set_index(0);
			// Else, go back to the introduction
			$('#intro_next.next').unbind();
			$(".slide").unbind();
			$('.next').unbind();
			$('input[name=q1]').attr('checked',false);
			$('input[name=q2]').attr('checked',false);
			$('input[name=q3]').attr('checked',false);
			alert("The answers that were given are incorrect. \n \nYou will be shown the instructions and slides again and have to repeat the comprehension check. \n\nOnce the answers are correct you can proceed to the next step.")
			CURRENTVIEW = new Instructions();
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
	$(".slide_trial").hide();
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

	// Start the experiment
	STATE = new State();
	CURRENTVIEW = new Instructions()
	// CURRENTVIEW = new Questions()
	// CURRENTVIEW = new TestPhase()
});