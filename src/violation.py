# -*- generated by 1.1.0b13 -*-
import da
PatternExpr_626 = da.pat.ConstantPattern('done')
PatternExpr_630 = da.pat.BoundPattern('_BoundPattern631_')
PatternExpr_632 = da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.TuplePattern([da.pat.FreePattern(None), da.pat.FreePattern(None), da.pat.BoundPattern('_BoundPattern638_')]), da.pat.ConstantPattern('done')])
_config_object = {}
import sys
# import fab
from prettytable import PrettyTable

def generate_config(prop_ids, acc_ids, lrn_ids):
    """
    This method generates the desired configuration required to reproduce the liveness violation
    discussed in the paper https://arxiv.org/pdf/1712.01367.pdf
    """
    config = dict()
    leader_conf = [{acc_ids[0], acc_ids[1], acc_ids[2]}, {acc_ids[3], acc_ids[0]}]
    acceptor_conf = [{acc_ids[0]: [acc_ids[1]], acc_ids[1]: [], acc_ids[2]: [acc_ids[1]], acc_ids[3]: []}, {acc_ids[0]: [], acc_ids[1]: [], acc_ids[2]: [], acc_ids[3]: []}]
    byzconf = {prop_ids[0]: 0, prop_ids[1]: 3, prop_ids[2]: 3, prop_ids[3]: 3}
    acc_rep_from = {acc_ids[0], acc_ids[1], acc_ids[3]}
    config['leader_config'] = {'propose_to': leader_conf}
    config['proposer_config'] = {'byzpropconf': byzconf}
    config['acceptor_config'] = {'accept_to': acceptor_conf, 'rep_from': acc_rep_from}
    return config

class Main(da.NodeProcess):

    def __init__(self, procimpl, forwarder, **props):
        super().__init__(procimpl, forwarder, **props)
        self._Node_ReceivedEvent_0 = []
        self._events.extend([da.pat.EventPattern(da.pat.ReceivedEvent, '_Node_ReceivedEvent_0', PatternExpr_626, sources=[PatternExpr_630], destinations=None, timestamps=None, record_history=True, handlers=[])])

    def run(self):
        """
        The main method for the class that drives Byzantine behaviour in the system.
        This is used to spawn Proposer, Acceptor and Learner processes 
        for the implementation. 
        Arguments for the number of proposers, acceptors, learners and byzantine processes
        will be specified during runtime.
        """
        f = (int(sys.argv[1]) if (len(sys.argv) > 1) else 1)
        p = (int(sys.argv[2]) if (len(sys.argv) > 2) else 4)
        a = (int(sys.argv[3]) if (len(sys.argv) > 3) else 4)
        l = (int(sys.argv[4]) if (len(sys.argv) > 4) else 4)
        lt = 20
        leaderelect = self.new(fab.Election)
        proposers = self.new(fab.Proposer, num=p)
        acceptors = self.new(fab.Acceptor, num=a)
        learners = self.new(fab.Learner, num=l)
        mode = 4
        proplist = list(proposers)
        acclist = list(acceptors)
        learnlist = list(learners)
        config = generate_config(proplist, acclist, learnlist)
        print('\n')
        print(('-' * 95))
        print(('#' * 29), 'REPRODUCTION OF LIVENESS VIOLATION', ('#' * 29))
        print(('-' * 95))
        table = PrettyTable(['Type of process', '1', '2', '3', '4'])
        lc = ['Proposers']
        for prop in proplist:
            lc.append(prop)
        table.add_row(lc)
        lc = ['Acceptors']
        for acc in acclist:
            lc.append(acc)
        table.add_row(lc)
        lc = ['Learners']
        for lrns in learnlist:
            lc.append(lrns)
        table.add_row(lc)
        print(table)
        print('\n')
        self._setup(leaderelect, (proplist, acceptors, p, f, mode, None))
        for proposer in proposers:
            self._setup(proposer, ((proposers - {proposer}), learners, acceptors, leaderelect, p, a, l, f, mode, config, None))
        for acceptor in acceptors:
            self._setup(acceptor, (learners, (acceptors - {acceptor}), leaderelect, a, f, mode, config, None))
        for learner in learners:
            self._setup(learner, (proposers, acceptors, (learners - {learner}), a, f, lt, mode, config, None))
        self._start(proposers)
        self._start(leaderelect)
        self._start(acceptors)
        self._start(learners)
        super()._label('_st_label_618', block=False)
        learner = None

        def UniversalOpExpr_619():
            nonlocal learner
            for learner in learners:
                if (not PatternExpr_632.match_iter(self._Node_ReceivedEvent_0, _BoundPattern638_=learner)):
                    return False
            return True
        _st_label_618 = 0
        while (_st_label_618 == 0):
            _st_label_618 += 1
            if UniversalOpExpr_619():
                _st_label_618 += 1
            else:
                super()._label('_st_label_618', block=True)
                _st_label_618 -= 1
        self.send('done', to=((proposers | acceptors) | learners))
        self.send('done', to=leaderelect)
