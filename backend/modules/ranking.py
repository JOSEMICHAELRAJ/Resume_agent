"""
ranking.py - Candidate Ranking Module
Combines multiple scoring metrics to rank candidates
"""

from utils.logger import app_logger


class CandidateRanker:
    """
    Ranks candidates based on multiple scoring criteria
    """
    
    # Weighting for different score components
    WEIGHTS = {
        'skill_match': 0.40,
        'experience_match': 0.25,
        'education_match': 0.15,
        'semantic_similarity': 0.20
    }
    
    def __init__(self):
        """Initialize the ranker"""
        self.weights = self.WEIGHTS
    
    def calculate_overall_score(self, scores):
        """
        Calculate overall score from component scores
        
        Args:
            scores: Dictionary with component scores
                - skill_match_score: 0-100
                - experience_match_score: 0-100
                - education_match_score: 0-100
                - semantic_similarity_score: 0-100
        
        Returns:
            Overall score 0-100
        """
        try:
            overall = (
                scores.get('skill_match_score', 0) * self.weights['skill_match'] +
                scores.get('experience_match_score', 0) * self.weights['experience_match'] +
                scores.get('education_match_score', 0) * self.weights['education_match'] +
                scores.get('semantic_similarity_score', 0) * self.weights['semantic_similarity']
            )
            
            return min(100, max(0, overall))  # Ensure score is between 0-100
        
        except Exception as e:
            app_logger.error(f"Error calculating overall score: {str(e)}")
            return 0
    
    def get_recommendation(self, overall_score, skill_match_percentage=0):
        """
        Get shortlist/reject recommendation based on score
        
        Args:
            overall_score: Overall ranking score
            skill_match_percentage: Percentage of required skills matched
        
        Returns:
            Recommendation string: 'SHORTLIST', 'PENDING', or 'REJECT'
        """
        if overall_score >= 75 and skill_match_percentage >= 70:
            return 'SHORTLIST'
        elif overall_score >= 60 and skill_match_percentage >= 50:
            return 'PENDING'
        else:
            return 'REJECT'
    
    def rank_candidates(self, candidates_scores):
        """
        Rank multiple candidates
        
        Args:
            candidates_scores: List of dictionaries with candidate scores
        
        Returns:
            Sorted list of candidates with recommendations
        """
        try:
            ranked_candidates = []
            
            for candidate_score in candidates_scores:
                overall_score = self.calculate_overall_score(candidate_score)
                
                recommendation = self.get_recommendation(
                    overall_score,
                    candidate_score.get('skill_match_percentage', 0)
                )
                
                ranked_candidate = {
                    **candidate_score,
                    'overall_score': overall_score,
                    'recommendation': recommendation,
                    'rank': None  # Will be assigned after sorting
                }
                
                ranked_candidates.append(ranked_candidate)
            
            # Sort by overall score
            ranked_candidates.sort(key=lambda x: x['overall_score'], reverse=True)
            
            # Assign ranks
            for i, candidate in enumerate(ranked_candidates, 1):
                candidate['rank'] = i
            
            app_logger.info(f"Ranked {len(ranked_candidates)} candidates")
            return ranked_candidates
        
        except Exception as e:
            app_logger.error(f"Error ranking candidates: {str(e)}")
            return []
    
    def get_ranking_summary(self, ranked_candidates):
        """
        Get summary statistics for ranked candidates
        
        Args:
            ranked_candidates: List of ranked candidates
        
        Returns:
            Summary dictionary
        """
        try:
            scores = [c['overall_score'] for c in ranked_candidates]
            recommendations = [c['recommendation'] for c in ranked_candidates]
            
            summary = {
                'total_candidates': len(ranked_candidates),
                'average_score': sum(scores) / len(scores) if scores else 0,
                'highest_score': max(scores) if scores else 0,
                'lowest_score': min(scores) if scores else 0,
                'shortlisted_count': recommendations.count('SHORTLIST'),
                'pending_count': recommendations.count('PENDING'),
                'rejected_count': recommendations.count('REJECT')
            }
            
            return summary
        
        except Exception as e:
            app_logger.error(f"Error generating ranking summary: {str(e)}")
            return {}
    
    def calculate_education_match(self, resume_education, required_education):
        """
        Calculate education match score
        
        Args:
            resume_education: List of education entries from resume
            required_education: Required education from JD
        
        Returns:
            Match score 0-100
        """
        try:
            if not resume_education:
                return 0
            
            if not required_education:
                return 100
            
            # Convert to lowercase for matching
            resume_ed_lower = [str(ed).lower() for ed in resume_education]
            required_ed_lower = str(required_education).lower()
            
            # Check for keyword matches
            degree_keywords = ['bachelor', 'master', 'phd', 'diploma', 'associate']
            
            score = 0
            for keyword in degree_keywords:
                if keyword in required_ed_lower:
                    # Check if resume has matching degree
                    for resume_ed in resume_ed_lower:
                        if keyword in resume_ed:
                            score = 100
                            break
                    
                    if score == 0:
                        # Partial credit for having some education
                        score = 50
                    break
            
            # If required education not specific, any education is good
            if score == 0 and resume_education:
                score = 60
            
            return score
        
        except Exception as e:
            app_logger.error(f"Error calculating education match: {str(e)}")
            return 0
