import os

exptdir = '003_collectstats_bilinear2_negKL'
script = 'train.py'
rootdir = '/scratch/jmj/vae_ssl/experiments/mnist_ssl_vae'
session = exptdir
savedir = os.path.join(rootdir,exptdir)

theano_flags='device=gpu{gpuid}'
run_flags=['--savedir=%s'%savedir,
           '--epochs=500',
           '-sfreq 50',
           '-betaprior 0.2',
           '--negKL=True',
           '--bilinear=True',
           '-nl maxout2',
           '-pl 3',
           '-ph 200',
           '-ql 3',
           '-qh 300',
           '-al 1',
           '-cw 128',
           '-lr 5e-4',
           '-ds 50',
           '-seed 1',
           '-rv 0.1']
vary_vals = {
        'BN':'--batchnorm=True --separateBNrunningstats=True',
        #'LN':'--layernorm=True',
        }

numgpus = 3
gpuctr = 2
for tag,val in vary_vals.iteritems():
    gpu = gpuctr % numgpus
    gpuctr += 1
    session_name = '%s_%s' % (session,tag)
    cmd='THEANO_FLAGS={theano_flags} python {script} {run_flags}'.format(
            theano_flags=theano_flags.format(gpuid=gpu),
            script=script,
            run_flags=' '.join(run_flags+[val]))
    execute = 'tmux new -d -s {session_name}; tmux send-keys -t {session_name} "{cmd}" Enter'.format(**locals())
    #execute = 'tmux kill-session -t {session_name}'.format(**locals())
    print execute
    os.system(execute)
    
