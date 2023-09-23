from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question, Vote
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class IndexView(generic.ListView):
    """
    View for displaying a list of latest questions.
    """
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')

class DetailView(generic.DetailView):
    """
    View for displaying details of a question.
    """
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
    
    def get(self, request, *args, **kwargs):
        """
        Handle GET request for detail view.
        """

        try:
            self.object = self.get_object()
        except Http404:
            return redirect('polls:index')
        
        if not self.object.can_vote():
            messages.error(request, 'The poll is not available.')
            return redirect('polls:index')
        
        user = request.user
        try:
            # Retrieve the current vote of the user for this question
            current_vote = self.object.choice_set.filter(vote__user=user).last()
        except TypeError:
            current_vote = None
        context = self.get_context_data(object=self.object, current_vote=current_vote)
        return self.render_to_response(context)
        

class ResultsView(generic.DetailView):
    """
    View for displaying the results of a question.
    """
    model = Question
    template_name = 'polls/results.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        Handle GET request for results view.
        """
        try:
            self.object = self.get_object()
        except Http404:
            return redirect('polls:index')
        if not self.object.is_published():
            messages.error(request, 'The poll is not available.')
            return redirect('polls:index')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

@login_required
def vote(request, question_id):
    """
    View for handling user votes on a question.
    """
    question = get_object_or_404(Question, pk=question_id)

    if not question.can_vote():
        messages.error(request, 'The poll is not available.')
        return redirect("polls:index")
    
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    
    this_user = request.user

    try:
        # find a vote for this user and this question
        vote = Vote.objects.get(user=this_user, choice__question=question)
        # update his vote
        vote.choice = selected_choice
    except Vote.DoesNotExist:
        #no matching vote - create a new Vote
        vote = Vote(user=this_user, choice=selected_choice)
    vote.save()
    # Add message after user successfully vote.
    messages.success(request, 'Your vote has been saved.')
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def get_client_ip(request):
    """Get the visitor’s IP address using request headers."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip