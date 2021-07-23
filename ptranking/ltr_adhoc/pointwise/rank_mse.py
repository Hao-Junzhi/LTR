#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Description
Viewing the prediction of relevance as a conventional regression problem.
"""

import torch
import torch.nn.functional as F

from ptranking.base.ranker import NeuralRanker


def rankMSE_loss_function(batch_pred=None, batch_label=None, TL_AF=None):
	'''
	Ranking loss based on mean square error
	:param batch_pred:
	:param batch_stds:
	:return:
	'''
	if 'S' == TL_AF or 'ST' == TL_AF:  # map to the same relevance level
		max_rele_level = torch.max(batch_label)
		batch_pred = batch_pred * max_rele_level

	batch_loss = F.mse_loss(batch_pred, batch_label)
	return batch_loss

class RankMSE(NeuralRanker):
	def __init__(self, sf_para_dict=None, gpu=False, device=None):
		super(RankMSE, self).__init__(id='RankMSE', sf_para_dict=sf_para_dict, gpu=gpu, device=device)
		self.TL_AF = self.get_tl_af()

	def inner_train(self, batch_pred, batch_label, **kwargs):
		'''
		:param batch_preds: [batch, ranking_size] each row represents the relevance predictions for documents within a ltr_adhoc
		:param batch_stds: [batch, ranking_size] each row represents the standard relevance grades for documents within a ltr_adhoc
		:return:
		'''
		batch_loss = rankMSE_loss_function(batch_pred, batch_label, TL_AF=self.TL_AF)

		self.optimizer.zero_grad()
		batch_loss.backward()
		self.optimizer.step()

		return batch_loss
