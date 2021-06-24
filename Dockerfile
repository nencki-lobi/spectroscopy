FROM openmrslab/openmrslab


#LCModel
WORKDIR /home/jovyan/
RUN wget -qO- http://s-provencher.com/pub/LCModel/programs/lcm-64.tar | tar -xv -C $HOME
RUN tar xzf $HOME/lcm-core.tar.gz -C $HOME
RUN rm  -f  $HOME/.lcmodel/doc/manual.ps
RUN rm  -f  $HOME/.lcmodel/gelx/preprocessors/fix-3t-bandwidth
RUN mkdir  -p  $HOME/.lcmodel/profiles/1
RUN touch $HOME/.lcmodel/license
RUN rm -f $HOME/install-lcmodel $HOME/.uninstall-lcmodel $HOME/lcm-core.tar.gz $HOME/lcm-64.tar

USER $NB_USER
RUN /bin/bash -c "source activate python2 && pip install pygamma"